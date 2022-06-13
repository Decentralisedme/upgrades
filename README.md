Lesson 12 from PatrickAlphaC:
- https://github.com/smartcontractkit/full-blockchain-solidity-course-py

Two contracts have been created:
A. Box >> retrieve and store functions
B. BoxV2 >> retrieve, store and increment functions

We want:
1. deploy A
2. store some value
3. Upgrade From A => B
4. Increment the already stored value

This is peroformed via OpenZeppelin proxy contracts:
- ProxyAdmin
- TransparentUpradeableProxy

The contracts have been deployed and verified in Rinkeby and as result Upgrade + Store + Increment have all been done via proxy, as you can see: 
- https://rinkeby.etherscan.io/address/0x13ff473c6253966a6b3454e0c00ab70f14470e6f

Tests have been run as well.