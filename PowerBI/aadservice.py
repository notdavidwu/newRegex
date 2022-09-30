import msal
'''Returns report embed uration'''
AUTHENTICATION_MODE = 'ServicePrincipal'
# Workspace Id in which the report is present
WORKSPACE_ID = '7c6c9886-7fc8-42bb-8dff-ae28b2a4c77d'
# Report Id for which Embed token needs to be generated
REPORT_ID = 'e572b80b-05c6-41f3-b331-d40706b2f35c'
# Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
TENANT_ID = 'be4937e1-5c7a-4f12-bd7f-cc51a82d238b' 
# Client Id (Application Id) of the AAD app
CLIENT_ID = '2916a788-a3f5-4dee-a7a7-5811ef212e9c'
# Client Secret (App Secret) of the AAD  Required only for ServicePrincipal authentication mode.
CLIENT_SECRET = 'JYB8Q~bRVNA73_i_VMgvcIzbWYhr5aKxNsmGTbVJ'
# Scope Base of AAD  Use the below uration to use all the permissions provided in the AAD app through Azure portal.
SCOPE_BASE = ['https://analysis.windows.net/powerbi/api/.default']
# URL used for initiating authorization request
AUTHORITY_URL = 'https://login.microsoftonline.com/organizations'
# Master user email address. Required only for MasterUser authentication mode.
POWER_BI_USER = ''
# Master user email password. Required only for MasterUser authentication mode.
POWER_BI_PASS = ''
class AadService:
    def get_access_token():
        '''Generates and returns Access token
        Returns:
            string: Access token
        '''
        response = None
        try:
            if AUTHENTICATION_MODE.lower() == 'masteruser':
                # Create a public client to authorize the app with the AAD app
                clientapp = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY_URL)
                accounts = clientapp.get_accounts(username=POWER_BI_USER)
                if accounts:
                    # Retrieve Access token from user cache if available
                    response = clientapp.acquire_token_silent(SCOPE_BASE, account=accounts[0])
                if not response:
                    # Make a client call if Access token is not available in cache
                    response = clientapp.acquire_token_by_username_password(POWER_BI_USER, POWER_BI_PASS, scopes=SCOPE_BASE)     
            # Service Principal auth is the recommended by Microsoft to achieve App Owns Data Power BI embedding
            elif AUTHENTICATION_MODE.lower() == 'serviceprincipal':
                authority = AUTHORITY_URL.replace('organizations', TENANT_ID)
                clientapp = msal.ConfidentialClientApplication(CLIENT_ID, client_credential=CLIENT_SECRET, authority=authority)

                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_for_client(scopes=SCOPE_BASE)
            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])
        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))