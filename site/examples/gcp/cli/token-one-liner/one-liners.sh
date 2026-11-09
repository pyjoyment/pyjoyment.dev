# The credentials of the user, which the Application Default Credentials find
gcloud auth application-default login

# The access token, as gcloud auth application-default print-access-token
python -c 'import Pyjo.GCP.Credentials.Chain as adc; print(adc.new().credentials().token)'

# The same with Workload Identity Federation, the token of the STS of Google for the one of another identity provider,
# of the file of gcloud iam workload-identity-pools create-cred-config
GOOGLE_APPLICATION_CREDENTIALS=wif.json python -c 'import Pyjo.GCP.Credentials.Chain as adc; print(adc.new().credentials().token)'

# Who the token is of, its scopes and its expiration, of the tokeninfo endpoint of Google
python -m Pyjo 'g("https://oauth2.googleapis.com/tokeninfo", form={"access_token": sys.argv[1]}).json()' "$(gcloud auth application-default print-access-token)"

# The project of the credentials, of gcloud config set project for a user, and its buckets of Cloud Storage
python -c 'import Pyjo.GCP.Credentials.Chain as adc; print(adc.new().credentials().project)'
python -c 'import Pyjo.GCP.Call as C, Pyjo.GCP.Client as G; print(G.new(service="storage").call(C.new("GET", "/storage/v1/b", query={"project": "myproject"})))'

# A token of a service account that the user impersonates, as gcloud auth print-access-token --impersonate-service-account
python -c 'import Pyjo.GCP.Credentials.Chain as adc, Pyjo.GCP.Credentials.Impersonated as i; print(i.new(source=adc.new(), target_principal="reader@myproject.iam.gserviceaccount.com").credentials().token)'
