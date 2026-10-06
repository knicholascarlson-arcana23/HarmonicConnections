<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Geometric Tonality Diamond & Exporter</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #111; color: #fff; margin: 0; padding: 20px; }
        h2 { margin-top: 0; color: #00aaff; margin-bottom: 5px; }
        .controls { background: #222; padding: 15px; border-radius: 8px; margin-bottom: 15px; display: flex; gap: 15px; align-items: center; flex-wrap: wrap; }
        input[type="text"], input[type="number"] { background: #333; color: #fff; border: 1px solid #555; padding: 8px; font-size: 15px; border-radius: 4px; font-family: monospace; }
        button { background: #00aaff; color: #111; border: none; padding: 8px 16px; font-size: 15px; font-weight: bold; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #0088cc; }
        .btn-export { background: #44ff44; }
        .btn-export:hover { background: #22cc22; }
        .help-text { width: 100%; color: #aaa; font-size: 13px; margin-top: 5px; font-weight: bold; }
        
        .container { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }
        .table-container { flex: 1.2; min-width: 350px; max-height: 500px; overflow-y: auto; background: #222; border-radius: 8px; padding: 10px; border: 1px solid #333; }
        table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
        th, td { padding: 8px 6px; border-bottom: 1px solid #444; }
        th { color: #00aaff; position: sticky; top: 0; background: #222; z-index: 10; }
        
        tr.clickable { 
            cursor: pointer; 
            transition: background 0.2s; 
            user-select: none; 
            -webkit-user-select: none; 
            -webkit-touch-callout: none;
        }
        tr.clickable:hover { background: #333; }
        
        tr.playing { background-color: rgba(68, 255, 68, 0.15) !important; }
        tr.playing td { border-bottom: 1px solid #44ff44; }
        
        #network-wrapper { flex: 2; min-width: 400px; height: 500px; background: #1a1a1a; border-radius: 8px; border: 1px solid #333; position: relative; }
        #mynetwork { 
            width: 100%; height: 100%; outline: none; 
            -webkit-touch-callout: none; 
        }
        
        #fullscreen-btn { position: absolute; top: 10px; right: 10px; background: rgba(0, 170, 255, 0.8); color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; z-index: 100; font-size: 12px; }
        :fullscreen #network-wrapper { width: 100vw; height: 100vh; border-radius: 0; border: none; }

        .basket-section { background: #222; padding: 15px; border-radius: 8px; border: 1px solid #444; }
        .basket-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #444; padding-bottom: 10px; margin-bottom: 10px; }
        .basket-header h3 { margin: 0; color: #ff8844; }
        .chip-container { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; min-height: 40px; }
        .chip { background: #444; border: 1px solid #666; padding: 5px 10px; border-radius: 15px; font-size: 14px; cursor: pointer; font-family: monospace; user-select: none; -webkit-user-select: none; }
        .chip:hover { background: #ff4444; color: white; border-color: #ff4444; }
        .chip::after { content: " ×"; opacity: 0.5; }
        .export-controls { display: flex; gap: 15px; flex-wrap: wrap; align-items: center; background: #1a1a1a; padding: 10px; border-radius: 6px; }
    </style>
</head>
<body>

    <h2>Geometric Tonality Diamond & Scale Exporter</h2>
    <div class="controls">
        <label title="Define prime limits and iterations (e.g., '3:2, 5:1' means prime 3 up to power 2, and prime 5 up to power 1)"><strong>Limits & Iterations:</strong></label>
        <input type="text" id="prime-input" value="3:2, 5:1" title="Define prime limits and iterations (e.g., '3:2, 5:1' means prime 3 up to power 2, and prime 5 up to power 1)">
        <button onclick="generateDiamond()" title="Generate the geometric Tonality Diamond graph and data table">Draw Diamond</button>
        <label style="display:flex; align-items:center; gap:5px; cursor:pointer; background:#333; padding:8px; border-radius:4px;" title="Toggle node labels between exact cents and nearest Western pitch (assuming 1/1 = C)">
            <input type="checkbox" id="pitch-toggle" onchange="generateDiamond()"> Pitches (1/1=C)
        </label>
        
        <!-- SAVE AND LOAD BUTTONS -->
        <button style="background:#00aaff; color:#111; margin-left: 10px;" onclick="saveWorkspace()" title="Save your Diamond configuration and selected basket">💾 Save</button>
        <button style="background:#ff8844; color:#111;" onclick="document.getElementById('workspace-upload').click()" title="Load a saved Diamond configuration">📂 Load</button>
        <input type="file" id="workspace-upload" accept=".json" style="display:none;" onchange="loadWorkspace(event)">

        <button onclick="stopAllAudio()" style="background:#555; margin-left: 10px;" title="Silence all currently playing pitch drones">🔇 Stop Drones</button>
        <div class="help-text">👆 TAP (or Left-Click) to Add/Remove from Basket. LONG-HOLD (or Right-Click) to toggle audio drones!</div>
    </div>

    <div class="container">
        <div class="table-container" title="Tap a row to add/remove. Long-Hold a row to audition pitch.">
            <table id="data-table">
                <thead><tr><th>Ratio</th><th>Cents</th><th>Nearest Pitch</th><th>Prime DNA</th></tr></thead>
                <tbody><!-- JS injects data here --></tbody>
            </table>
        </div>
        
        <div id="network-wrapper">
            <button id="fullscreen-btn" onclick="toggleFullScreen()" title="Expand the geometric graph to fill the entire screen">⛶ Full Screen</button>
            <div id="mynetwork" title="Interactive Graph: Tap node to add/remove. Long-Hold to audition pitch."></div>
        </div>
    </div>

    <div class="basket-section">
        <div class="basket-header">
            <h3 title="Your selected scale. These ratios will be exported.">🛒 Custom Scale Basket</h3>
            <button onclick="basket.clear(); updateBasketUI();" style="background: #555;" title="Remove all selected ratios from your basket (resets to just 1/1)">Clear Basket</button>
        </div>
        <div class="chip-container" id="basket-chips" title="Your selected scale. These ratios will be exported.">
            <!-- Chips injected here -->
        </div>
        
        <div class="export-controls">
            <label title="Set the exact frequency in Hertz for the 1/1 fundamental (e.g., 261.63 for Middle C)"><strong>1/1 Freq (Hz):</strong> <input type="number" id="base-freq" value="261.6256" step="0.01" style="width:100px;" title="Set the exact frequency in Hertz for the 1/1 fundamental (e.g., 261.63 for Middle C)"></label>
            <label title="Set the MIDI note number that corresponds to your 1/1 fundamental (e.g., 60 for Middle C)"><strong>Root MIDI Note:</strong> <input type="number" id="root-midi" value="60" min="0" max="127" style="width:60px;" title="Set the MIDI note number that corresponds to your 1/1 fundamental (e.g., 60 for Middle C)"></label>
            <button class="btn-export" onclick="exportCSV()" title="Export a detailed spreadsheet mapping your custom scale across all 128 keys">Download 128-Key CSV</button>
            <button class="btn-export" onclick="exportScala()" title="Export a standard Scala (.scl) tuning file to import into synthesizers or your Workstation">Download Scala (.scl)</button>
            <button class="btn-export" onclick="exportSCAMP()" title="Export a JSON dictionary of pitch offsets for use in algorithmic composition libraries like Python SCAMP">Download Python Dict</button>
        </div>
    </div>

    <script>
        const PITCH_NAMES = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"];
        
        let network = null;
        let networkNodes = new vis.DataSet();
        let networkEdges = new vis.DataSet();
        let diamondDataMap = new Map(); 
        let basket = new Set(["1/1"]); 
        
        let audioCtx = null;
        let playingAudio = new Map();

        // --- IOS AUDIO UNLOCKER ---
        function unlockAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            const silentOsc = audioCtx.createOscillator();
            const silentGain = audioCtx.createGain();
            silentGain.gain.value = 0;
            silentOsc.connect(silentGain);
            silentGain.connect(audioCtx.destination);
            silentOsc.start();
            silentOsc.stop(audioCtx.currentTime + 0.01);

            document.body.removeEventListener('touchstart', unlockAudio);
            document.body.removeEventListener('pointerdown', unlockAudio);
            document.body.removeEventListener('click', unlockAudio);
        }
        
        document.body.addEventListener('touchstart', unlockAudio, { once: true });
        document.body.addEventListener('pointerdown', unlockAudio, { once: true });
        document.body.addEventListener('click', unlockAudio, { once: true });

        // --- WORKSPACE SAVE & LOAD LOGIC ---
        function saveWorkspace() {
            let state = {
                primeInput: document.getElementById("prime-input").value,
                baseFreq: document.getElementById("base-freq").value,
                rootMidi: document.getElementById("root-midi").value,
                showPitches: document.getElementById("pitch-toggle").checked,
                basket: Array.from(basket)
            };
            let jsonStr = JSON.stringify(state, null, 2);
            downloadFile("Diamond_Workspace.json", jsonStr);
        }

        function loadWorkspace(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    let state = JSON.parse(e.target.result);
                    if (state.primeInput) document.getElementById("prime-input").value = state.primeInput;
                    if (state.baseFreq) document.getElementById("base-freq").value = state.baseFreq;
                    if (state.rootMidi) document.getElementById("root-midi").value = state.rootMidi;
                    if (state.showPitches !== undefined) document.getElementById("pitch-toggle").checked = state.showPitches;
                    
                    // Redraw the diamond based on the loaded inputs
                    generateDiamond();
                    
                    // Repopulate the basket
                    if (state.basket) {
                        basket = new Set(state.basket);
                        updateBasketUI();
                    }
                } catch (err) {
                    alert("Invalid Workspace File");
                }
            };
            reader.readAsText(file);
            event.target.value = ''; // Reset input so you can load the same file again if needed
        }

        // --- LONG PRESS STATE FOR TABLE ROWS ---
        let rowPressTimer = null;
        let rowLongPressed = false;

        function startRowPress(e, ratioStr) {
            if (e.button === 2) return; 
            
            rowLongPressed = false;
            rowPressTimer = setTimeout(() => {
                rowLongPressed = true;
                toggleRatioSound(ratioStr);
                if (navigator.vibrate) navigator.vibrate(50);
            }, 500); 
        }

        function endRowPress(e, ratioStr) {
            if (e.button === 2) return; 
            clearTimeout(rowPressTimer);
            if (!rowLongPressed) {
                toggleBasket(ratioStr);
            }
        }

        function cancelRowPress() {
            clearTimeout(rowPressTimer);
        }

        // --- VISUAL FEEDBACK ENGINE ---
        function setNodePlayingVisuals(ratioStr, isPlaying) {
            if (networkNodes.get(ratioStr)) {
                let defaultBg = (ratioStr === "1/1") ? "#00aaff" : "#333";
                let defaultText = (ratioStr === "1/1") ? "#111" : "#fff";
                
                networkNodes.update({
                    id: ratioStr,
                    color: { 
                        background: isPlaying ? "#44ff44" : defaultBg, 
                        border: isPlaying ? "#fff" : "#555" 
                    },
                    font: { color: isPlaying ? "#111" : defaultText }
                });
            }
            
            let row = document.querySelector(`tr[data-ratio="${ratioStr}"]`);
            if (row) {
                if (isPlaying) { row.classList.add('playing'); } 
                else { row.classList.remove('playing'); }
            }
        }

        // --- POLYPHONIC AUDIO ENGINE ---
        function toggleRatioSound(ratioStr) {
            if (!audioCtx) unlockAudio();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            
            if (playingAudio.has(ratioStr)) {
                let nodes = playingAudio.get(ratioStr);
                nodes.gainNode.gain.setValueAtTime(nodes.gainNode.gain.value, audioCtx.currentTime);
                nodes.gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.3); 
                nodes.osc.stop(audioCtx.currentTime + 0.35);
                playingAudio.delete(ratioStr);
                
                setNodePlayingVisuals(ratioStr, false);
            } else {
                let [num, den] = ratioStr.split('/').map(Number);
                let baseFreq = parseFloat(document.getElementById("base-freq").value) || 261.6256;
                let targetFreq = baseFreq * (num / den);

                let osc = audioCtx.createOscillator();
                osc.type = "triangle"; 
                osc.frequency.setValueAtTime(targetFreq, audioCtx.currentTime);

                let gainNode = audioCtx.createGain();
                gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
                
                let maxVol = 0.15; 
                gainNode.gain.linearRampToValueAtTime(maxVol, audioCtx.currentTime + 0.1); 

                osc.connect(gainNode);
                gainNode.connect(audioCtx.destination);

                osc.start();
                playingAudio.set(ratioStr, { osc: osc, gainNode: gainNode });
                
                setNodePlayingVisuals(ratioStr, true);
            }
        }

        function stopAllAudio() {
            if (!audioCtx) return;
            playingAudio.forEach((nodes, ratioStr) => {
                nodes.gainNode.gain.setValueAtTime(nodes.gainNode.gain.value, audioCtx.currentTime);
                nodes.gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.1);
                nodes.osc.stop(audioCtx.currentTime + 0.15);
                setNodePlayingVisuals(ratioStr, false);
            });
            playingAudio.clear();
        }

        // --- MATH HELPERS ---
        function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }
        function reduceToOctave(num, den) {
            let n = num, d = den;
            while (n / d >= 2) d *= 2;
            while (n / d < 1) n *= 2;
            let g = gcd(n, d);
            return { n: n / g, d: d / g };
        }
        function extractOddPrimes(n) {
            let factors = new Set();
            while (n % 2 === 0) n /= 2;
            for (let i = 3; i * i <= n; i += 2) {
                while (n % i === 0) { factors.add(i); n /= i; }
            }
            if (n > 1) factors.add(n);
            return Array.from(factors).sort((a,b)=>a-b);
        }
        function parseIdentities(rawStr) {
            let factors = {};
            rawStr.split(",").forEach(item => {
                item = item.trim();
                if (item.includes(":")) {
                    let parts = item.split(":");
                    factors[parseInt(parts[0])] = parseInt(parts[1]);
                } else if(item && !isNaN(item)) { factors[parseInt(item)] = 1; }
            });
            let identities = [1];
            for (const [p, count] of Object.entries(factors)) {
                let newIds = [];
                for (let i = 0; i <= count; i++) {
                    identities.forEach(val => newIds.push(val * Math.pow(p, i)));
                }
                identities = newIds;
            }
            return [...new Set(identities)].sort((a,b)=>a-b);
        }

        function toggleFullScreen() {
            let elem = document.getElementById("network-wrapper");
            if (!document.fullscreenElement) { elem.requestFullscreen(); } 
            else { document.exitFullscreen(); }
        }

        function toggleBasket(ratioStr) {
            if (basket.has(ratioStr) && ratioStr !== "1/1") { basket.delete(ratioStr); } 
            else { basket.add(ratioStr); }
            updateBasketUI();
        }

        function getSortedBasket() {
            return Array.from(basket).sort((a, b) => {
                let [n1, d1] = a.split('/').map(Number);
                let [n2, d2] = b.split('/').map(Number);
                return (n1/d1) - (n2/d2);
            });
        }

        function updateBasketUI() {
            let container = document.getElementById("basket-chips");
            container.innerHTML = "";
            let sorted = getSortedBasket();
            if (sorted.length === 0) { container.innerHTML = "<span style='color:#777;'>Basket is empty. Tap a node to add.</span>"; return; }
            
            sorted.forEach(ratio => {
                let chip = document.createElement("div");
                chip.className = "chip";
                chip.innerText = ratio;
                chip.title = `Click to remove ${ratio} from the basket`; 
                chip.onclick = () => { if (ratio !== "1/1") toggleBasket(ratio); };
                container.appendChild(chip);
            });
        }

        function generateDiamond() {
            stopAllAudio(); 

            let rawInput = document.getElementById("prime-input").value;
            let showPitches = document.getElementById("pitch-toggle").checked;
            let identities = parseIdentities(rawInput);
            let N = identities.length;
            
            networkNodes.clear();
            networkEdges.clear();
            diamondDataMap.clear();

            for (let r = 0; r < N; r++) {
                for (let c = 0; c < N; c++) {
                    let otonal = identities[r], utonal = identities[c];
                    let reduced = reduceToOctave(otonal, utonal);
                    let ratioStr = `${reduced.n}/${reduced.d}`;
                    let exactCents = 1200 * Math.log2(reduced.n / reduced.d);
                    
                    let nearestSemitone = Math.round(exactCents / 100) % 12;
                    let roundedCentsTarget = Math.round(exactCents / 100) * 100;
                    let offset = exactCents - roundedCentsTarget;
                    let sign = offset >= 0 ? "+" : "";
                    let pitchStr = `${PITCH_NAMES[nearestSemitone]} ${sign}${offset.toFixed(1)}c`;

                    let sigNum = extractOddPrimes(reduced.n);
                    let sigDen = extractOddPrimes(reduced.d);
                    let fullSig = `${sigNum.length ? sigNum.join(",") : "1"} / ${sigDen.length ? sigDen.join(",") : "1"}`;

                    let xPos = (c - r) * 90;
                    let yPos = (c + r) * 60;
                    let nodeId = ratioStr; 

                    let displayLabel = showPitches ? `${pitchStr}\n(${ratioStr})` : `${ratioStr}\n(${exactCents.toFixed(1)}c)`;

                    if (!diamondDataMap.has(ratioStr)) {
                        diamondDataMap.set(ratioStr, { id: ratioStr, cents: exactCents.toFixed(2), pitch: pitchStr, primeDNA: fullSig });
                        
                        networkNodes.add({
                            id: nodeId,
                            label: displayLabel,
                            x: xPos, y: yPos, fixed: true, shape: "box",
                            color: { background: ratioStr === "1/1" ? "#00aaff" : "#333", border: '#555', hover: { background: '#ff8844' } },
                            font: { color: ratioStr === "1/1" ? "#111" : "#fff", face: "monospace" },
                            title: `Ratio: ${ratioStr} | Cents: ${exactCents.toFixed(2)}c\nTap: Add to scale | Long-Hold: Toggle audio drone` 
                        });
                    }

                    if (r < N - 1) networkEdges.add({ from: nodeId, to: `${reduceToOctave(identities[r+1], utonal).n}/${reduceToOctave(identities[r+1], utonal).d}`, color: '#ff6666', width: 2 });
                    if (c < N - 1) networkEdges.add({ from: nodeId, to: `${reduceToOctave(otonal, identities[c+1]).n}/${reduceToOctave(otonal, identities[c+1]).d}`, color: '#66aa66', width: 2 });
                }
            }

            let tableData = Array.from(diamondDataMap.values()).sort((a, b) => a.cents - b.cents);
            let tbody = document.querySelector("#data-table tbody");
            tbody.innerHTML = "";
            tableData.forEach(d => {
                tbody.innerHTML += `<tr class="clickable" data-ratio="${d.id}" 
                    onpointerdown="startRowPress(event, '${d.id}')" 
                    onpointerup="endRowPress(event, '${d.id}')" 
                    onpointerleave="cancelRowPress()" 
                    onpointercancel="cancelRowPress()" 
                    oncontextmenu="toggleRatioSound('${d.id}'); event.preventDefault(); return false;" 
                    title="Tap: Toggle in Basket | Long-Hold: Toggle audio drone">
                    <td><strong>${d.id}</strong></td>
                    <td>${d.cents}c</td>
                    <td style="color: #4da6ff; font-weight: bold;">${d.pitch}</td>
                    <td style="color: #ff8844; font-family: monospace;">${d.primeDNA}</td>
                </tr>`;
            });

            let container = document.getElementById("mynetwork");
            let data = { nodes: networkNodes, edges: networkEdges };
            let options = {
                physics: false,
                interaction: { hover: true, dragNodes: false, zoomView: true, dragView: true }
            };
            
            if (network) network.destroy();
            network = new vis.Network(container, data, options);
            
            let networkHeld = false;

            network.on("hold", function (params) {
                let nodeId = network.getNodeAt(params.pointer.DOM);
                if (nodeId) { 
                    networkHeld = true;
                    toggleRatioSound(nodeId); 
                    if (navigator.vibrate) navigator.vibrate(50);
                }
            });

            network.on("click", function (params) {
                if (networkHeld) {
                    networkHeld = false; 
                    return;
                }
                if (params.nodes.length > 0) { toggleBasket(params.nodes[0]); }
            });

            network.on("oncontext", function (params) {
                params.event.preventDefault(); 
                let nodeId = network.getNodeAt(params.pointer.DOM);
                if (nodeId) { toggleRatioSound(nodeId); }
            });

            updateBasketUI();
        }

        function downloadFile(filename, content) {
            let blob = new Blob([content], { type: 'text/plain' });
            let link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            link.click();
        }

        function exportCSV() {
            let sortedRatios = getSortedBasket();
            let baseFreq = parseFloat(document.getElementById("base-freq").value);
            let rootMidi = parseInt(document.getElementById("root-midi").value);
            let scaleSize = sortedRatios.length;
            
            let csvContent = "MIDI Note,Mapped Ratio,Frequency (Hz),Nearest 12-TET Note,Cent Offset (+/-)\n";

            for (let i = 0; i <= 127; i++) {
                let diff = i - rootMidi;
                let octaveShift = Math.floor(diff / scaleSize);
                let degree = ((diff % scaleSize) + scaleSize) % scaleSize; 
                
                let ratioStr = sortedRatios[degree];
                let [num, den] = ratioStr.split('/').map(Number);
                let ratioFloat = num / den;
                
                let exactFreq = baseFreq * ratioFloat * Math.pow(2, octaveShift);
                let exactMidiFloat = 69 + 12 * Math.log2(exactFreq / 440);
                let nearestMidi = Math.round(exactMidiFloat);
                let offsetCents = (exactMidiFloat - nearestMidi) * 100;
                
                let pitchName = PITCH_NAMES[nearestMidi % 12];
                let octaveNum = Math.floor(nearestMidi / 12) - 1;
                
                csvContent += `${i},${ratioStr} (x2^${octaveShift}),${exactFreq.toFixed(3)},${pitchName}${octaveNum} (${nearestMidi}),${offsetCents >= 0 ? '+' : ''}${offsetCents.toFixed(2)}c\n`;
            }
            downloadFile("Acoustic_128_Key_Mapping.csv", csvContent);
        }
        
        function exportScala() {
            let sortedRatios = getSortedBasket();
            let outNotes = sortedRatios.filter(ratio => ratio !== "1/1");
            
            if (!outNotes.includes("2/1")) {
                outNotes.push("2/1");
            }
            
            let scaleSize = outNotes.length;
            
            let sclContent = "!\n";
            sclContent += "Custom Diamond Scale\n";
            sclContent += ` ${scaleSize}\n`;
            sclContent += "!\n";
            
            outNotes.forEach(ratio => {
                sclContent += ` ${ratio}\n`;
            });
            
            downloadFile("Custom_Diamond_Scale.scl", sclContent);
        }
        
        function exportSCAMP() {
            let sortedRatios = getSortedBasket();
            let dictObj = {};
            
            sortedRatios.forEach(ratio => {
                let [num, den] = ratio.split('/').map(Number);
                let semitones = 12 * Math.log2(num / den);
                dictObj[ratio] = parseFloat(semitones.toFixed(4));
            });
            
            let jsonStr = JSON.stringify(dictObj, null, 4);
            downloadFile("SCAMP_Tuning_Dict.json", jsonStr);
        }

        window.onload = generateDiamond;
    </script>
</body>
</html>
