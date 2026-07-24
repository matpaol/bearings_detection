# bearings_detection

Diagnosi di guasti ai cuscinetti di motori a induzione tramite **Deep Autoencoder + 1-D CNN**
sui segnali di corrente di statore del dataset Paderborn.
Progetto per il corso di Macchine ed Azionamenti Elettrici (UNIVPM).

## Struttura

```
bearings_detection/
  README.md
  01_dataset_exploration.ipynb   comprensione del dataset
  requirements.txt
  utils/
    config.py          parametri del progetto (un solo posto)
    repository.py      accesso al repository remoto (list, download, extract)
    dataset.py         lettura e catalogazione (BearingMetadata, load_signal, census)
    preprocessing.py   segnale -> frame (segmentazione per giro, ricampionamento, standardizzazione)
    plots.py           visualizzazioni
```

Il principio: **il notebook orchestra, i moduli in `utils/` lavorano**.

## Come si esegue (Google Colab)

1. Apri `01_dataset_exploration.ipynb` in Colab.
2. Esegui la cella di setup: installa le dipendenze, fa `git clone` del repo e `from utils import ...`.
3. Runtime -> Run all.

In locale: `pip install -r requirements.txt`, poi apri il notebook dalla radice del repo.

## Dipendenze

numpy, scipy, pandas, matplotlib, pymupdf; piu il pacchetto di sistema `unrar`.
