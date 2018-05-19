dict = {"id": [1, 2],
       "queryTag": ["Sales_Output", "Profit_Output"],
       "sub": ["sales","profit"],
       "emailId": ["mijaganiya@gmail.com,a@ex.com","mijaganiya@gmail.com"],   #update emails
       "query": ["select * from data where total_sales>500;","select * from data where total_profit>50;"] ,
       "cronTime": [0.1,4] , # Cron in Minutes
       "active": [1,1] 
        }

def dic():
        return dict
