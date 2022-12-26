"""
AWS Functions Below
"""

import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd

# requires your own keys 
ACCESS_KEY = ''
SECRET_KEY = ''

# simplify by removing the list comp to remove the filter
def get_all_files_in_bucket_filter(filtr):
    keys = []
    
    session = boto3.Session( 
             aws_access_key_id=ACCESS_KEY, 
             aws_secret_access_key=SECRET_KEY)

    #Then use the session to get the resource
    s3 = session.resource('s3')

    my_bucket = s3.Bucket('webpagebucket77')

    for my_bucket_object in my_bucket.objects.all():
        keys.append((my_bucket_object.key))

    newlist = [x for x in keys if filtr in x]
    print(newlist)

def delete_dynomodb(log_id):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('TABLE-NAME')
    response = table.delete_item(Key={"LogID": str(log_id)})
    return True
  
def get_from_dynomo():
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('TABLE-NAME')
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    # print(data)
    df = pd.DataFrame(data)
    return df
  

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

"""
How to genrate a QR code
"""
import qrcode
import hashlib

def create_qr_code(data):
    """
    Create a QR code from a string.
    """
    path = "Desktop/"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = hashlib.md5(data.encode()).hexdigest() + ".png"
    img.save(path+filename)
    
    return filename


"""
How to genrate a semi random number
"""

# random uuid for logging or other non exact ids needed
import uuid

def get_random_id(size):
    unquie_id = str(uuid.uuid4().hex)
    return unquie_id[:size]

"""
Creating url for google maps directrions from two points
"""
def googlemaps():
    start_google = str(coord[0])+','+str(coord[1])
    end_google = (result["lat"])+','+(result["log"])
    paylod = """ '"""+start_google+"""'/'"""+end_google+"""' """

    return "https://www.google.com/maps/dir/"+payload



"""
send an email using python
"""

import smtplib
import ssl
from email.message import EmailMessage
def sendemail(body,subject):

    email_sender = 'example@gmail.com'
    email_password = 'example'
    email_receiver = 'example@gmail.com'

    subject = 'SCRIPT UPDATE'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())    



"""
Creating a python graph simple example
"""


# load in relevent data then:

import plotly.express as px
   
fig = px.bar(df_master_two, x="Date", y="RuntimeALG",
             color="typeTwo", hover_data=['typeTwo'],
             barmode = 'group')
   
fig.show()

"""
Basic Network X graph example
"""

import networkx as nx
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)
nx.draw(G)


"""
Basic web scarapping example using beautiful soup
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = Letting_web_URL
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

bed_element = soup.find_all("h2", class_="prop_title no_line-height white")
for bed in bed_element:
    bed_val = bed.text.strip()
    bed_val = bed_val[0]

job_elements = soup.find_all("div", class_="prop_info")

for job_element in job_elements:
    bed_element = job_element.find("h2", class_="prop_address no_line-height blue")
    price_element = job_element.find("span", itemprop="price")
    price_element = price_element["content"]
    title_element = job_element.find("h2", class_="prop_address no_line-height blue")
    links = job_element.find("a", class_="list_link")
    link_url = links["href"]

    link_val = str("https://www.lettingweb.com/"+str(link_url))
    title_element = (title_element.text.strip())

    lendf =len(df_of_val)
    df_of_val.loc[lendf,'street_name'] = title_element
    df_of_val.loc[lendf,'street_link'] = link_val
    df_of_val.loc[lendf,'website'] = 'lettingweb'
    df_of_val.loc[lendf,'price_element'] = price_element
    df_of_val.loc[lendf,'bed_num'] = bed_val
