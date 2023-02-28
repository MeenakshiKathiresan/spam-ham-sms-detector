# Spam/Ham sms detector  
A spam/ham dataset from kaggle was used to train with random forest model. The model had an accuracy of 98% when tested against the test subset from the dataset. The model was saved and used within the flask web app. The flask app was deployed on AWS elastic bean stalk. Parallely, a free twilio account was created and a free mobile number was activated. The deployed app’s link was given to the twilio account’s web hook so that everytime a message is sent to the number, the web hook is triggered and the flask app will respond back with the prediction. The message logs were stored on AWS dynamodb. Along with the prediction, the users were also asked if the prediction was correct. The users can reply back by evaluating the prediction. The evaluation will also be stored in the database. This way on more misclassifications, the model can be retrained and deployed.

![image2](https://user-images.githubusercontent.com/26730019/221911003-2c6c7f16-b625-4f98-8253-8aa97311a37c.png)

# To test it
Send an sms to the deployed number and get a prediction if the sent message is spam or ham. You can validate the prediction with 'correct' or 'wrong'.  

![output-onlinepngtools (2)](https://user-images.githubusercontent.com/26730019/221911863-535ae551-dfb6-4b29-aa5f-060bb10061ed.png)


(Suspended twilio account and it is not live)

# Tech stack
- Python
- Jupyter notebooks
- Twilio API
- flask
- AWS dynamodb
- AWS elastic bean stalk

# Reference
https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset 
