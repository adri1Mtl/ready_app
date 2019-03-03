# ready_app

In order to run this locally, you need to install tornado: pip install tornado

You will also need to download the Dogs of NYC CSV file and put it in the same location as index.py. 

Run "python index.py" and go to "localhost:5000". You should see the application running.

The application is deployed here: http://adri1mtl.pythonanywhere.com/

You can do a count request: http://adri1mtl.pythonanywhere.com/count?dog_name=Buddy&gender=f

Run the test script with "READY_TEST_BASE_URL=http://adri1mtl.pythonanywhere.com python apitest.py" in bash. 

One test will fail because of the header "Content-Type	application/json; charset=UTF-8". The test wants "application/json" only, but the set_header() function in Tornado adds the "charset=UTF-8". According to RFC 4627, "JSON text shall be encoded in Unicode. The default encoding is UTF-8." (https://www.ietf.org/rfc/rfc4627.txt).

The other tests should succeed.

Have a nice day,

Adrien

