
python -m grpc_tools.protoc -I. --python_out=./frontend --grpc_python_out=./frontend ./proto/discovery.proto
python -m grpc_tools.protoc -I. --python_out=./frontend --grpc_python_out=./frontend ./proto/login.proto
python -m grpc_tools.protoc -I. --python_out=./frontend --grpc_python_out=./frontend ./proto/searchforecast.proto
python -m grpc_tools.protoc -I. --python_out=./frontend --grpc_python_out=./frontend ./proto/searchnow.proto
python -m grpc_tools.protoc -I. --python_out=./frontend --grpc_python_out=./frontend ./proto/searchpast.proto


python -m grpc_tools.protoc -I. --python_out=./api-gateway --grpc_python_out=./api-gateway ./proto/discovery.proto
python -m grpc_tools.protoc -I. --python_out=./api-gateway --grpc_python_out=./api-gateway ./proto/login.proto
python -m grpc_tools.protoc -I. --python_out=./api-gateway --grpc_python_out=./api-gateway ./proto/searchforecast.proto
python -m grpc_tools.protoc -I. --python_out=./api-gateway --grpc_python_out=./api-gateway ./proto/searchnow.proto
python -m grpc_tools.protoc -I. --python_out=./api-gateway --grpc_python_out=./api-gateway ./proto/searchpast.proto


python -m grpc_tools.protoc -I. --python_out=./login --grpc_python_out=./login ./proto/login.proto
python -m grpc_tools.protoc -I. --python_out=./search-forecast --grpc_python_out=./search-forecast ./proto/searchforecast.proto
python -m grpc_tools.protoc -I. --python_out=./search-now --grpc_python_out=./search-now ./proto/searchnow.proto
python -m grpc_tools.protoc -I. --python_out=./search-past --grpc_python_out=./search-past ./proto/searchpast.proto

python -m grpc_tools.protoc -I. --python_out=./login --grpc_python_out=./login ./proto/discovery.proto
python -m grpc_tools.protoc -I. --python_out=./search-forecast --grpc_python_out=./search-forecast ./proto/discovery.proto
python -m grpc_tools.protoc -I. --python_out=./search-now --grpc_python_out=./search-now ./proto/discovery.proto
python -m grpc_tools.protoc -I. --python_out=./search-past --grpc_python_out=./search-past ./proto/discovery.proto