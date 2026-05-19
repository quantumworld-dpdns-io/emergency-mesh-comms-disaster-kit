# System Overview

```
[Phone PWA] <--WS/REST--> [FastAPI API] --> [Mesh App Loop]
                                   |         |-> [Router Algorithms]
                                   |         |-> [Transport Manager: UDP/TCP/LoRa/...]
                                   |         |-> [AI Coordinator]
                                   |
                +------------------+---------------------------+
                |                  |                           |
             [Redis]            [DuckDB]                   [Qdrant]
                |                  |                           |
          pub/sub + locks      analytics + ETL            RAG knowledge
```
