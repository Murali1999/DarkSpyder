# Research about dark net

## Performing proxy-chaining using CONNECT method
- Proxy chaining is the process of sending a request through multiple proxy servers to reach the final destination. In this method, each proxy server acts as a 
client for the next server in the chain.
- To perform proxy chaining using the Connect HTTP method, you can use a client that supports the HTTP Connect method and allows you to configure multiple proxy servers. 
For example, the cURL command line tool can be used to perform proxy chaining with the following syntax:
```
curl --proxy <proxy1>:<port1> --proxy-connect-timeout <timeout> --proxy-tunnel --proxy-user <username>:<password> --proxy <proxy2>:<port2> -U <username>:<password> <url>
```
- In the above command:
  - --proxy <proxy1>:<port1> is the first proxy server you want to send the request through.
  - --proxy-connect-timeout <timeout> sets the timeout for the connection to the first proxy server.
  - --proxy-tunnel specifies that the connection should be treated as a tunnel.
  - --proxy-user <username>:<password> is the username and password for the first proxy server if it requires authentication.
  - --proxy <proxy2>:<port2> is the second proxy server in the chain.
  - -U <username>:<password> is the username and password for the second proxy server if it requires authentication.
  - <url> is the URL of the final destination you want to reach.
- Example:
```
curl --proxy proxy1.example.com:8080 --proxy-connect-timeout 10 --proxy-tunnel --proxy-user user1:pass1 --proxy proxy2.example.com:8080 -U user2:pass2 https://www.example.com/
```
- In this example, the request is sent through two proxy servers, proxy1.example.com and proxy2.example.com, and it takes up to 10 seconds to connect to the first proxy server. Both proxy servers require authentication, and the credentials for each server are specified with --proxy-user and -U. The final destination is https://www.example.com/.
