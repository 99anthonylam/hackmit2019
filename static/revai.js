function doStream() {
    finalsReceived = 0;
    currentCell = document.getElementById("journal-entry");
    audioContext = new (window.AudioContext || window.WebkitAudioContext)();

    const access_token = '02IWjeF81FK7flskRFjghrh0ZlBKxgV0xf2hvUNfUgsdTxmr2ZDoHZydmcLOycqludbEOK0UaeM166YFV_zH69VGdqNIU';
    const content_type = `audio/x-raw;layout=interleaved;rate=${audioContext.sampleRate};format=S16LE;channels=1`;
    const baseUrl = 'wss://api.rev.ai/speechtotext/v1alpha/stream';
    const query = `access_token=${access_token}&content_type=${content_type}`;
    websocket = new WebSocket(`${baseUrl}?${query}`);

    websocket.onopen = onOpen;
    websocket.onmessage = onMessage;
    websocket.onerror = console.error;

    var button = document.getElementById("streamButton");
    button.onclick = endStream;
    button.innerHTML = "Stop";
}

function endStream() {
    if (websocket) {
        websocket.send("EOS");
        websocket.close();
    }
    if (audioContext) {
        audioContext.close();
    }

    var button = document.getElementById("streamButton");
    button.onclick = doStream;
    button.innerHTML = "Record";
}

function onOpen(event) {
    navigator.mediaDevices.getUserMedia({ audio: true }).then((micStream) => {
        audioContext.suspend();
        var scriptNode = audioContext.createScriptProcessor(4096, 1, 1 );
        var input = input = audioContext.createMediaStreamSource(micStream);
        scriptNode.addEventListener('audioprocess', (event) => processAudioEvent(event));
        input.connect(scriptNode);
        scriptNode.connect(audioContext.destination);
        audioContext.resume();
    });
}

function onMessage(event) {
    var data = JSON.parse(event.data)
    switch (data.type){
        case "partial":
            break;
        case "final":
            var final = parseResponse(data);
            if (data.type == "final"){
                finalsReceived++;
                currentCell.value = currentCell.value + " " + final;
            }
            break;
        default:
            console.error("Received unexpected message");
            break;
    }
}

function processAudioEvent(e) {
    if (audioContext.state === 'suspended' || audioContext.state === 'closed' || !websocket) {
        return;
    }

    let inputData = e.inputBuffer.getChannelData(0);

    let output = new DataView(new ArrayBuffer(inputData.length * 2));
    for (let i = 0; i < inputData.length; i++) {
        let multiplier = inputData[i] < 0 ? 0x8000 : 0x7fff;
        output.setInt16(i * 2, inputData[i] * multiplier | 0, true);
    }

    let intData = new Int16Array(output.buffer);
    let index = intData.length;
    while (index-- && intData[index] === 0 && index > 0) { }
    websocket.send(intData.slice(0, index + 1));
}

function parseResponse(response) {
    var message = "";
    for (var i = 0; i < response.elements.length; i++){
        message += response.type == "final" ?  response.elements[i].value : `${response.elements[i].value} `;
    }
    return message;
}
