import logging
import boto3
import boto3.session
from concurrent import futures
import json
import time
import grpc
import controller_pb2
import controller_pb2_grpc

HOST = '[::]:8080'
my_session = boto3.session.Session()

archivo = open('archivo.txt', 'w')
oldInstances=[]
newInstances=[]

resource_ec2 = boto3.client("ec2", 
                            aws_access_key_id="ASIA5KF4RYNQQJ7BWOUH",
                            aws_secret_access_key="Lxuhfw/1QbplOPLiGVdcV3mZysdm11iJdEksyDVV",
                            aws_session_token="FwoGZXIvYXdzEDEaDDSofgEtCoULlhPnYCLIAXh0RZwJrFppEd0BgIb1DbdWAMyAEB+gSRuakWd3F7SU96QokZd81Tj+r1XUkL7AVQMKiLnFv8Zomx8tGyLV6s/8niMcCTOsXTBRvAjDA5c6jtZs91dL3XQkFJ1YR0aUSP0fIX28BNWRW1pxJcDTO/JL+0q5bhBR8KCd2JU1xBEyrI3+nXNZyMd1j9rfgsni5qROvapb9tROvF6GrQxruaS4s1/83iJcoLY9jI0IQXCMZQ68slJzMGAlf5OwRS4c6FKJqmFfJvBKKIbik6MGMi3714yu6tchfkRxGZA64fHfomou8lwyYqhADsbTofRZO5zXQ/e1O+lm9e60IBo=",
                            region_name='us-east-1')

lt = {
    'LaunchTemplateId': 'lt-0b369b2430457df2b',
}

def create_ec2_instance():
    get_old_instances()
    try:
        print ("Creating EC2 instance")
        resource_ec2.run_instances(
            LaunchTemplate=lt,
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="TeleKey")
        time.sleep(1)
        get_new_instance()
        
    except Exception as e:
        print(e)

def get_old_instances():
    try:
        response = resource_ec2.describe_instances()
        # Recorrer la respuesta y obtener la IP de cada instancia
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceId'] not in oldInstances:
                    oldInstances.append(instance['InstanceId'])
    except Exception as e:
        print(e)

def get_new_instance():
    try:
        response = resource_ec2.describe_instances()
        # Recorrer la respuesta y obtener la IP de cada instancia
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                actualid=instance['InstanceId']
                if actualid not in oldInstances:
                    newInstances.append(instance['InstanceId'])
    except Exception as e:
        print(e)

def get_ipv4(instance_id):
    response = resource_ec2.describe_instances(InstanceIds=[instance_id])
    ipv4_publico = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    return ipv4_publico

def terminate_ec2_instance(instance_id):
    try:
        archivo.write("Terminate EC2 instance")
        print("Terminate EC2 instance")
        util=resource_ec2.terminate_instances(InstanceIds=[instance_id])
        archivo.write(util)
        print(util)
        newInstances.remove(instance_id)
        return "Instancia " + instance_id+ " terminada"
    except Exception as e:
        print(e)
        return 

def minimum_instances():
    if len(newInstances)<2:
        while len(newInstances)<2: 
            create_ec2_instance()
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def Ping(ipv4_publica):
    with grpc.insecure_channel(ipv4_publica+":8080") as channel:
        stub = controller_pb2_grpc.controllerStub(channel)
        response = stub.Ping(controller_pb2.Nada())
    return response
def serve():
    with open('archivo.txt', 'w') as archivo:
        archivo.truncate()
    starttime = time.time()
    minimum_instances()
    print("waiting for instances to launch")
    archivo.write("waiting for instances to launch")
    time.sleep(180)
    while True:
        minimum_instances()
        for instance in newInstances:
            ip = get_ipv4(instance)
            try:
                response= Ping(ip)
                if response.status_code==0:
                    print(ip+" esta activa y la ocupacion de su cpu es de "+ str(response.cpu_usage))
                    archivo.write(ip+" esta activa y la ocupacion de su cpu es de "+ str(response.cpu_usage))
                    if response.cpu_usage>50 and response.cpu_usage<80:
                        if len(newInstances)<4:
                            create_ec2_instance()
                    elif response.cpu_usage>80:
                        terminate_ec2_instance(instance)
            except:
                print(ip+" esta prendiendo")
                archivo.write(ip+" esta prendiendo")
            
        time.sleep(30.0-((time.time() - starttime)%30.0))

def serve2():
    starttime = time.time()
    while True:
        ip ="3.93.20.58"
        try:
            response= Ping(ip)
            if response.status_code==0:
                print(ip+" esta activa y la ocupacion de su cpu es de "+ str(response.cpu_usage))
                
                if response.cpu_usage>50 and len(newInstances)<4 and response.cpu_usage<80:
                    #create_ec2_instance()
                    print("hola")
                elif response.cpu_usage>80:
                    #terminate_ec2_instance(instance)
                    print("hola")
        except Exception as e:
            print(e)
        
        time.sleep(5.0-((time.time() - starttime)%5.0))        
if __name__ == '__main__':
    logging.basicConfig()
    serve()
