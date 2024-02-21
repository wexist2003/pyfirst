from time import sleep
import time
import pika


from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def send_email(contact_id):
    print(f'Sending email to contact with ID: {contact_id}')
    time.sleep(1)
    Contact.objects(id=contact_id).update_one(set__sent_email=True)
    print(f'Mark email sent for contact with ID: {contact_id}')
    

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_email(contact_id)
    print(f'Done for: {contact_id}')


channel.basic_consume(queue='email_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
