# Face Compare com Facenet 

| Python | 3.9 |
| :---: | :---: |


Este é um repositório contém uma implementação do TensorFlow com o um face recognizer descrito no artigo "FaceNet: A Unified Embedding for Face Recognition and Clustering". 

## Executando com docker

The package and any of the example notebooks can be run with docker (or nvidia-docker) using:

```bash
docker build -t face_compare:latest .
docker run -p 5001:5000 -d face_compare:latest
```
## Processando a comparação de imagens

Em: [Face Compare API](http://localhost:5001/)

Informe duas imagens em base64 para comparação. O resultado é o retorno do objeto:

```

Prediction {
    match*	boolean
        Indicador que essas imagens são da mesma pessoa ou não
    threshold*	number
        Valor limite de classificação usado para determinar se eles são a mesma pessoa ou não.
    distance*	number
        A distância entre duas imagens em relação ao threshold
}

```


## Referências

1. F. Schroff, D. Kalenichenko, J. Philbin. _FaceNet: A Unified Embedding for Face Recognition and Clustering_, arXiv:1503.03832, 2015. [PDF](https://arxiv.org/pdf/1503.03832)


