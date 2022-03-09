# Author: Christine Pham
# Date: Dec 4, 2021
bags = "bags"
items = "items"
users = "users"

########---------------------JWT VERIFICATION START--------------------
# Update the values of the following 3 variables
CLIENT_ID = 'GmZ2IwzN1hKJZKmtaZklI6ePxK8X368k' #'YOUR_CLIENT_ID'
CLIENT_SECRET = 'icS-v8knNLsPrtO2CUH1u4Y0X_EuR3fu0y_plVG5xiJzukf6nG7rNnBweJWgB63E' #'YOUR_CLIENT_SECRET'
DOMAIN = '493f-portfolio.us.auth0.com' #YOUR_AUTH0_DOMAIN'
# For example
# DOMAIN = 'fall21.us.auth0.com'

ALGORITHMS = ["RS256"]

def get_secret():
    return '15Zvzk3p0rvrEusL58ho'