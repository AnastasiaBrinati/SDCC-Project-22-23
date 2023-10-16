python -m grpc_tools.protoc -I. --python_out=./login --grpc_python_out=./login ./proto/discovery.proto
python -m grpc_tools.protoc -I. --python_out=./frontend --grpc_python_out=./frontend ./proto/discovery.proto
python -m grpc_tools.protoc -I. --python_out=./api-gateway --grpc_python_out=./api-gateway ./proto/discovery.proto

python -m grpc_tools.protoc -I. --python_out=./frontend --grpc_python_out=./frontend ./proto/login.proto
python -m grpc_tools.protoc -I. --python_out=./login --grpc_python_out=./login ./proto/login.proto
python -m grpc_tools.protoc -I. --python_out=./api-gateway --grpc_python_out=./api-gateway ./proto/login.proto