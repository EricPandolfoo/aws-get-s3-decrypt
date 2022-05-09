# aws-get-s3-decrypt

## Este código busca um objeto criptografado do S3, decriptografa o objeto e publica o conteúdo em um tópico SNS ##

## OBS: o trigger desta lambda é uma fila SQS, por isso "for record in event['Records']" ##
