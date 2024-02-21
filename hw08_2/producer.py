import pika

from datetime import datetime
from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='email_mock', exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='email_mock', queue='email_queue')


def main():
    for i in range(20):
            contact = Contact(
                fullname=f'Contact {i+1}',
                email=f'contact{i+1}@example.com',
                sent_email=False 
            )
            contact.save()
            channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))

    print(f'20 contacts generated and sent to the email queue.')
    connection.close()
    
    
if __name__ == '__main__':
    main()
