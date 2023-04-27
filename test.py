import os
import json
import datetime
import pendulum
from pathlib import Path
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonVirtualenvOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import sys
from os.path import basename


# Set Path
this_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(this_dir, os.pardir))
#result_path = this_dir + '/results/'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))



# Fetching info from Airflow Env Variables:
var_mkt_reports_parameters = Variable.get("secret_mkt_wbr_automation_parameters") 
mkt_reports_param          = json.loads(var_mkt_reports_parameters)
mkt_daily_session_summary  = mkt_reports_param["mkt_wbr_parameters"]
snowflake_database = mkt_daily_session_summary["snowflake_database"] 
snowflake_schema = mkt_daily_session_summary["snowflake_schema"]
files = []

def from_file(file_name):
    try:
        with open(file_name, 'r') as sql_file:
            sql_file_output = sql_file.read()
        return sql_file_output
    except FileNotFoundError:
        print("Error processing file: file [%s] not found." % file_name)
        raise
    except Exception as e:
        print("Error processing file [%s]." % file_name)
        raise

acq_deep_dive = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra2/wbr_acq_deep_dive.sql")).format(snowflake_database, snowflake_schema)

ccp_with_factor = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra2/wbr_ccp_with_factor.sql")).format(snowflake_database, snowflake_schema)

ccp_without_factor = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra2/wbr_ccp_without_factor.sql")).format(snowflake_database, snowflake_schema)
    
email_addressable_market = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra1/wbr_email_addressable_market.sql")).format(snowflake_database, snowflake_schema)
    
hva_mc2 = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra1/wbr_hva_mc2.sql")).format(snowflake_database, snowflake_schema)
    
mc1_churn_reactivation = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra2/wbr_mc1_churn_reactivation.sql")).format(snowflake_database, snowflake_schema)

order_cancellation = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra2/wbr_order_cancellation.sql")).format(snowflake_database, snowflake_schema)
    
paid_rx_orders = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra1/wbr_paid_Rx_orders.sql")).format(snowflake_database, snowflake_schema) 
    
active_subscribers = from_file(Path(Path(Path(os.path.realpath(__file__)).parent, "sql"),
    "wbr_automation/infra1/wbr_As_Active_Subscribers.sql")).format(snowflake_database, snowflake_schema)   
    
def process_queries(**kwargs):
    import io
    import os
    import re
    import json
    import boto3
    import datetime
    import zipfile
    import csv

    config    = kwargs['key1']
    proc_name = kwargs['key2']
    proc_start_date = kwargs['key3']
    proc_start_time = kwargs['key4']
    module    = kwargs['key5']
    step_name = kwargs['key6']
    step_start_dt = kwargs['key7']
    step_start_tm = kwargs['key8']
    step_end = kwargs['key9']
    download = kwargs['key10']
    destination = kwargs['key11']
    bucket_name = kwargs['key12']

    from mkt_connectors.monitor import Monitor
    from mkt_connectors.config  import configure
    from mkt_connectors.secret  import get_secret
    from mkt_connectors.snowflake import SnowflakeDatabase
    #from wbr_email_notification.email_notifier import EmailClient
    #from mkt_notifier.services.emailer import EmailClient

    get_secret = get_secret(config["secret_name"])
    config.update(get_secret)
    config_opt = configure(conf_options=config)
    monitoring = Monitor(config_opt)

    
    if module == "start":
        try:
            monitoring.insert_process_metadata(proc_start_date, proc_start_time, proc_name)
        except Exception as e:
            print(f"********************* error: ********************* {e}")
            monitoring.update_process_metadata(process_name=proc_name,
                                               process_start_date=proc_start_date,
                                               process_start_time=proc_start_time,
                                               process_end_time=datetime.datetime.now(),
                                               time_taken=(
                                                       datetime.datetime.now().timestamp() -
                                                       proc_start_time.timestamp()),
                                               status='Failed',
                                               notes=json.dumps(re.sub(r"\W+|_", " ", str(e)))
                                               )
            raise ValueError("Error executing insert process: " + str(e))
    elif module == "end":
        try:
            print(f"********************* module: ********************* {module}")
            monitoring.update_process_metadata(proc_start_date, proc_start_time, proc_name, 'Success',
                                               datetime.datetime.now(),
                                               json.dumps("None"),
                                               datetime.datetime.now().timestamp() - proc_start_time.timestamp(), )
        except Exception as e:
            print(f"********************* error: ********************* {e}")
            monitoring.update_process_metadata(process_name=proc_name,
                                               process_start_date=proc_start_date,
                                               process_start_time=proc_start_time,
                                               process_end_time=datetime.datetime.now(),
                                               time_taken=(
                                                       datetime.datetime.now().timestamp() -
                                                       proc_start_time.timestamp()),
                                               status='Failed',
                                               notes=json.dumps(re.sub(r"\W+|_", " ", str(e)))
                                               )
            raise ValueError("Error executing update process: " + str(e))
    elif module == "email":
        try:
            zipped_file = io.BytesIO()

            with zipfile.ZipFile(zipped_file, 'w') as zipper:
        
                for i, csv_file in enumerate(files):
                    csv_file[1].seek(0)
                    zipper.writestr(zipfile.ZipInfo(csv_file[0]+".csv"), csv_file[1].read())
            
            with open("wbr_files.zip", "wb") as f: 
                f.write(zipped_file.getvalue())
                
            s3_client.put_object(
                Bucket = bucket_name,
                Body   = zipped_file.getvalue(),
                Key    = "WBR/acq_deep_dive.zip"
            )
            zipped_file.seek(0)  
            #email_client = EmailClient(smtp_server=None)
            monitoring.update_process_metadata(proc_start_date, proc_start_time, proc_name, 'Success',
                                               datetime.datetime.now(),
                                               json.dumps("None"),
                                               datetime.datetime.now().timestamp() - proc_start_time.timestamp(),attachment=zipped_file.getvalue(),attachment_name='WBR ZIP', )
        except Exception as e:
                return {"message": f"unable to connect to SMTP server: {e}"}, 503
        monitoring.process_success_alert_notification(process_name='imp_email_notifier', notes='WBR weekly file is here', attachment=zipped_file.getvalue(), attachment_name='WBR ZIP test',)
       
    else:
        try:
            monitoring.insert_step_metadata(step_start_dt, step_start_tm, proc_name, step_name)
            print(f'>> Running Query -- {module}<<')
            snowflake = SnowflakeDatabase(config_opt)
            if download:
                result_DF   = snowflake.get_data(module)
                csv_buffer = io.StringIO()
                result_DF.to_csv(csv_buffer,index=False)
                session     = boto3.session.Session(region_name='us-east-1')
                s3_client   = session.client('s3')
                s3_client.put_object(
                    Bucket = bucket_name,
                    Body   = csv_buffer.getvalue().encode('utf-8'),
                    Key    = destination
                )
                
                #csv_buffer = StringIO()
                #writer = csv.writer(csv_buffer)
                #writer.writerow(["some", "csv", "data"])

                #csv_buffer.seek(0)
                
                files.append([module,csv_buffer])
                
                # s3_client.put_object(
                #     Bucket = bucket_name,
                #     Body   = "acq_deep_dive.zip",
                #     Key    = "WBR/acq_deep_dive_temp.zip"
                # )
                # zipped_file.seek(0)

            else:
                snowflake.execute_query(module)
            monitoring.update_step_metadata(step_start_dt, step_start_tm, proc_name, step_name, 'Success', step_end,
                                            datetime.datetime.now().timestamp() - step_start_tm.timestamp(),
                                            json.dumps("None"))
        except Exception as e:
            payload = f"Error occurred while executing SQL query in Snowflake: {e}"
            monitoring.update_step_metadata(
                step_start_date=step_start_dt,
                step_start_time=step_start_tm,
                process_name=proc_name,
                step_name=step_name, status='Failed',
                notes=json.dumps(re.sub(r"\W+|_", " ", (str(e))))
            )

            monitoring.update_process_metadata(process_name=proc_name,
                                               process_start_date=proc_start_date,
                                               process_start_time=proc_start_time,
                                               process_end_time=datetime.datetime.now(),
                                               time_taken=(
                                                       datetime.datetime.now().timestamp() - proc_start_time.timestamp()),
                                               status='Failed',
                                               notes=json.dumps(re.sub(r"\W+|_", " ", str(e)))
                                               )
            raise ValueError(payload)



# Setting Process Details:
process_name       = 'wbr_results_automation'
process_start_time = datetime.datetime.now()
process_start_date = process_start_time.date()

with DAG(
    dag_id='mkts_wbr_weekly',
    default_args={
            "owner": "Marketing Solution",
            "depends_on_past": False,
            "retries": 0,
            "start_date": pendulum.datetime(2023, 3, 1, tz="America/New_York"),
            "max_active_runs": 1,
        },
schedule_interval="0 14 * * MON",
    tags=["version: 1.1.1"],
    catchup=False
) as dag:

    proc_start = PythonVirtualenvOperator(
        task_id="process_start",
        python_callable=process_queries,
        requirements=["mkt-connectors"],
        system_site_packages=False,
        op_kwargs={
            "key1": mkt_daily_session_summary,
            "key2": process_name,
            "key3": process_start_date,
            "key4": process_start_time,
            "key5": "start",
            "key6": "",
            "key7": "",
            "key8": "",
            "key9": "",
            "key10":False,
            "key11":"",
            "key12":""
        }
    )

    proc_end = PythonVirtualenvOperator(
        task_id="process_end",
        python_callable=process_queries,
        requirements=["mkt-connectors"],
        system_site_packages=False,
        op_kwargs={
            "key1": mkt_daily_session_summary,
            "key2": process_name,
            "key3": process_start_date,
            "key4": process_start_time,
            "key5": "end",
            "key6": "",
            "key7": "",
            "key8": "",
            "key9": "",
            "key10":False,
            "key11":"",
            "key12":""
        }
    )

    step_start_date = datetime.datetime.now().date()
    step_start_time = datetime.datetime.now()
    step_end_date   = datetime.datetime.now()

    RUN_DATE = (datetime.datetime.today() - datetime.timedelta(days=1)).date().strftime('%Y%m%d')

    FILENAME = f'{RUN_DATE}.csv'
    s3_BUCKET = 'dev-use1-bi-data-warehouse-mkt-solutions-api-repository'

    acq_deep_dive_call = PythonVirtualenvOperator(
        task_id="imp_acq_deep_dive",
        python_callable=process_queries,
        requirements=["mkt-connectors"],
        system_site_packages=False,
        op_kwargs={
            "key1": mkt_daily_session_summary,
            "key2": process_name,
            "key3": process_start_date,
            "key4": process_start_time,
            "key5": acq_deep_dive,
            "key6": "WBR_Data_Snowflake_to_s3",
            "key7": step_start_date,
            "key8": step_start_time,
            "key9": step_end_date,
            "key10": True,
            "key11":f'WBR/acq_deep_dive_{FILENAME}',
            "key12":s3_BUCKET
            
                   }
    )

    # ccp_with_factor_call = PythonVirtualenvOperator(
    #     task_id="imp_ccp_with_factor",
    #     python_callable=process_queries,
    #     requirements=["mkt-connectors","shutil"],
    #     system_site_packages=False,
    #     op_kwargs={
    #         "key1": mkt_daily_session_summary,
    #         "key2": process_name,
    #         "key3": process_start_date,
    #         "key4": process_start_time,
    #         "key5": ccp_with_factor,
    #         "key6": "WBR_Data_Snowflake_to_s3",
    #         "key7": step_start_date,
    #         "key8": step_start_time,
    #         "key9": step_end_date,
    #         "key10": True,
    #         "key11":f'WBR/ccp_with_factor{FILENAME}',
    #         "key12":s3_BUCKET

    #                }
    # )

    # ccp_without_factor_call = PythonVirtualenvOperator(
    #     task_id="imp_ccp_without_factor",
    #     python_callable=process_queries,
    #     requirements=["mkt-connectors"],
    #     system_site_packages=False,
    #     op_kwargs={
    #         "key1": mkt_daily_session_summary,
    #         "key2": process_name,
    #         "key3": process_start_date,
    #         "key4": process_start_time,
    #         "key5": ccp_without_factor,
    #         "key6": "WBR_Data_Snowflake_to_s3",
    #         "key7": step_start_date,
    #         "key8": step_start_time,
    #         "key9": step_end_date,
    #         "key10": True,
    #         "key11":f'WBR/ccp_without_factor{FILENAME}',
    #         "key12":s3_BUCKET

    #                }
    # )
    
    # email_addressable_market_call = PythonVirtualenvOperator(
    #     task_id="imp_email_addressable_market",
    #     python_callable=process_queries,
    #     requirements=["mkt-connectors"],
    #     system_site_packages=False,
    #     op_kwargs={
    #         "key1": mkt_daily_session_summary,
    #         "key2": process_name,
    #         "key3": process_start_date,
    #         "key4": process_start_time,
    #         "key5": email_addressable_market,
    #         "key6": "WBR_Data_Snowflake_to_s3",
    #         "key7": step_start_date,
    #         "key8": step_start_time,
    #         "key9": step_end_date,
    #         "key10": True,
    #         "key11":f'WBR/email_addressable_market{FILENAME}',
    #         "key12":s3_BUCKET

    #                }
    # )
    
    # hva_mc2_call = PythonVirtualenvOperator(
    #     task_id="imp_hva_mc2",
    #     python_callable=process_queries,
    #     requirements=["mkt-connectors"],
    #     system_site_packages=False,
    #     op_kwargs={
    #         "key1": mkt_daily_session_summary,
    #         "key2": process_name,
    #         "key3": process_start_date,
    #         "key4": process_start_time,
    #         "key5": hva_mc2,
    #         "key6": "WBR_Data_Snowflake_to_s3",
    #         "key7": step_start_date,
    #         "key8": step_start_time,
    #         "key9": step_end_date,
    #         "key10": True,
    #         "key11":f'WBR/hva_mc2{FILENAME}',
    #         "key12":s3_BUCKET

    #                }
    # )

    
    # mc1_churn_reactivation_call = PythonVirtualenvOperator(
    #     task_id="imp_mc1_churn_reactivation",
    #     python_callable=process_queries,
    #     requirements=["mkt-connectors"],
    #     system_site_packages=False,
    #     op_kwargs={
    #         "key1": mkt_daily_session_summary,
    #         "key2": process_name,
    #         "key3": process_start_date,
    #         "key4": process_start_time,
    #         "key5": mc1_churn_reactivation,
    #         "key6": "WBR_Data_Snowflake_to_s3",
    #         "key7": step_start_date,
    #         "key8": step_start_time,
    #         "key9": step_end_date,
    #         "key10": True,
    #         "key11":f'WBR/mc1_churn_reactivation{FILENAME}',
    #         "key12":s3_BUCKET

    #                }
    # )
    
    
    # order_cancellation_call = PythonVirtualenvOperator(
    #     task_id="imp_order_cancellation",
    #     python_callable=process_queries,
    #     requirements=["mkt-connectors"],
    #     system_site_packages=False,
    #     op_kwargs={
    #         "key1": mkt_daily_session_summary,
    #         "key2": process_name,
    #         "key3": process_start_date,
    #         "key4": process_start_time,
    #         "key5": order_cancellation,
    #         "key6": "WBR_Data_Snowflake_to_s3",
    #         "key7": step_start_date,
    #         "key8": step_start_time,
    #         "key9": step_end_date,
    #         "key10": True,
    #         "key11":f'WBR/order_cancellation{FILENAME}',
    #         "key12":s3_BUCKET

    #                }
    # )

    
    # paid_rx_orders_call = PythonVirtualenvOperator(
    #     task_id="imp_paid_Rx_orders",
    #     python_callable=process_queries,
    #     requirements=["mkt-connectors"],
    #     system_site_packages=False,
    #     op_kwargs={
    #         "key1": mkt_daily_session_summary,
    #         "key2": process_name,
    #         "key3": process_start_date,
    #         "key4": process_start_time,
    #         "key5": paid_rx_orders,
    #         "key6": "WBR_Data_Snowflake_to_s3",
    #         "key7": step_start_date,
    #         "key8": step_start_time,
    #         "key9": step_end_date,
    #         "key10": True,
    #         "key11":f'WBR/paid_Rx_orders{FILENAME}',
    #         "key12":s3_BUCKET

    #                }
    # )

    
    # active_subscribers_call = PythonVirtualenvOperator(
    #     task_id="imp_active_subscribers",
    #     python_callable=process_queries,
    #     requirements=["mkt-connectors"],
    #     system_site_packages=False,
    #     op_kwargs={
    #         "key1": mkt_daily_session_summary,
    #         "key2": process_name,
    #         "key3": process_start_date,
    #         "key4": process_start_time,
    #         "key5": active_subscribers,
    #         "key6": "WBR_Data_Snowflake_to_s3",
    #         "key7": step_start_date,
    #         "key8": step_start_time,
    #         "key9": step_end_date,
    #         "key10": True,
    #         "key11":f'WBR/As_active_subscribers{FILENAME}',
    #         "key12":s3_BUCKET

    #                }
    # )

    # task_download_from_s3 = PythonOperator(
    #     task_id='download_from_s3',
    #     python_callable=filedownload.main,
    #     op_kwargs={
    #         'key': f'WBR/active_subscribers{FILENAME}',
    #         'bucket_name': s3_BUCKET,
    #         'local_path': '/Users/dradecic/airflow/data/'
    #     }
    # )

    email_notifier_call = PythonVirtualenvOperator(
        task_id="imp_email_notifier",
        python_callable=process_queries,
        requirements=["mkt-connectors"],
        system_site_packages=False,
        op_kwargs={
            "key1": mkt_daily_session_summary,
            "key2": process_name,
            "key3": process_start_date,
            "key4": process_start_time,
            "key5": "email",
            "key6": "",
            "key7": step_start_date,
            "key8": step_start_time,
            "key9": step_end_date,
            "key10": False,
            "key11": 'WBR/wbr_files.zip',
            "key12": s3_BUCKET

                   }
    )


    proc_start >> acq_deep_dive_call >> email_notifier_call >> proc_end
    # proc_start >> ccp_with_factor_call >> proc_end
    # proc_start >> ccp_without_factor_call >> proc_end
    # proc_start >> email_addressable_market_call >> proc_end
    # proc_start >> hva_mc2_call >> proc_end
    # proc_start >> mc1_churn_reactivation_call >> proc_end
    # proc_start >> order_cancellation_call >> proc_end
    # proc_start >> paid_rx_orders_call >> proc_end
    # proc_start >> active_subscribers_call >> proc_end
    #proc_start >> email_notifier_call >> proc_end