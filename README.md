## How to use
Launch central node:
```bash
python3 central_node.py <CENTRAL_HOST> <CENTRAL_PORT>
```
Example:
```bash
python3 central_node.py 172.29.67.89 9000
```
Launch user node on specified port:
```bash
python3 user_node.py <CENTRAL_HOST> <CENTRAL_PORT> <PORT> <FILE_1_TO_SHARE> <FILE_2_TO_SHARE> ...
```
Example:
```bash
python3 user_node.py 172.29.67.89 9000 9001 share/pic-2.jpeg
```