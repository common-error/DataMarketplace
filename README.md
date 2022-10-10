# DataMarketplace

**Lanciare i comandi dalle relative cartelle**

## Comandi per l'avvio della simulazione
1. Avvio Blockchain
```
npx ganache-cli --deterministic
```
2. Avvio server front-end
```
python -m flask run
```

## Compilazione contratto
Comando per generare ABI del contratto.
Da utilizzare solo se si modifica il codice del contratto. 
**Ad ogni nuova compilazione riavviare il server front-end e la blockchain di testing**

Una volta compilato il nuovo bytecode:
1. Copiare il contenuto della chiave "ABI" nel json al percorso "smart-contract/build/contracts/accessAuth.json"
2. Incollare quanto copiato nella variabile chiamata "ABI" all'interno del file al percorso "flask-server/static/js/logic.js"
3. Copiare l'intero file al percorso "smart-contract/build/contracts/accessAuth.json" nella cartella ""owner-KeysManagement/ABI"

Comando per la compilazione
```
npx truffle compile
```
