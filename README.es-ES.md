

# EmosiFloww

Una plataforma descentralizada de cápsulas del tiempo para almacenar recuerdos digitales cifrados y desbloquearlos en un horario programado utilizando contratos inteligentes de blockchain.

## Características

* Almacenamiento multimedia con bloqueo temporal
* Cifrado AES-256 del lado del cliente
* Almacenamiento descentralizado usando Walrus
* Desbloqueo programado basado en contratos inteligentes
* Tokenización NFT ERC-721
* Integración con la billetera MetaMask
* Soporte para imágenes, videos, audio y documentos

## Stack Tecnológico

* **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS
* **Blockchain:** Ethereum Sepolia, Hedera SDK
* **Almacenamiento:** Walrus Protocol
* **Cifrado:** AES-256, SHA-256, PBKDF2
* **NFTs:** ERC-721
* **Web3:** ethers.js
* **UI:** Three.js, React Three Fiber, Motion

## Arquitectura

```text
Carga de Archivo
    ↓
Cifrado del Lado del Cliente
    ↓
Almacenamiento Descentralizado Walrus
    ↓
Bloqueo Temporal del Contrato Inteligente
    ↓
Acuñación de NFT ERC-721
    ↓
Descifrado Programado
```

## Instalación

```bash
git clone https://github.com/aaditya3301/EmosiFloww.git
cd EmosiFloww
npm install
cp .env.example .env.local
npm run dev
```

Abrir:

```text
http://localhost:3000
```

## Variables de Entorno

```env
WALRUS_PUBLISHER_URL=your_walrus_publisher_url
WALRUS_AGGREGATOR_URL=your_walrus_aggregator_url
ETHEREUM_RPC_URL=your_sepolia_rpc_url
TIME_CAPSULE_CONTRACT=your_contract_address
```

## Estructura del Proyecto

```text
EmosiFloww/
├── src/app/        # Páginas de Next.js
├── src/components/ # Componentes de UI
├── src/lib/        # Lógica de cifrado, NFT y blockchain
├── contracts/      # Contratos inteligentes en Solidity
└── public/         # Activos estáticos
```

## Licencia

Licenciado bajo la Licencia MIT.
