const fs = require('fs');
const file = './screens/Neural_Network_Engine.html';
let html = fs.readFileSync(file, 'utf8');

const oldSection = `        <!-- Input Image Viz -->
        <div class="glass-panel p-4 rounded-xl flex flex-col flex-1 min-h-[200px]">
             <span class="mono-tech text-[10px] text-zinc-500 uppercase mb-4">Input Vectorization</span>
             <div class="flex-1 flex flex-col items-center justify-center border border-white/5 rounded-lg bg-black/30 p-4 relative overflow-hidden font-mono text-[10px] text-zinc-400">
                  <!-- Mockup of a feature vector -->
                  <div class="grid grid-cols-3 gap-2 w-full text-center animate-pulse opacity-70">
                      <div class="bg-white/5 p-1 rounded text-yellow-400">[0.82]</div>
                      <div class="bg-white/5 p-1 rounded">[-0.15]</div>
                      <div class="bg-white/5 p-1 rounded text-red-400">[0.99]</div>
                      <div class="bg-white/5 p-1 rounded">[0.42]</div>
                      <div class="bg-white/5 p-1 rounded text-yellow-400">[0.75]</div>
                      <div class="bg-white/5 p-1 rounded">[-0.88]</div>
                      <div class="bg-white/5 p-1 rounded text-red-400">[0.91]</div>
                      <div class="bg-white/5 p-1 rounded">[0.11]</div>
                      <div class="bg-white/5 p-1 rounded">[-0.04]</div>
                  </div>
                  <div class="mt-4 text-xs tracking-widest uppercase text-white/50">User x Movie Tensor</div>
             </div>
        </div>`;

const newSection = `        <!-- Enhanced Input Vectorization Viz -->
        <div class="glass-panel p-5 rounded-xl flex flex-col gap-4">
            <!-- Header -->
            <div class="flex items-center justify-between">
                <div>
                    <span class="mono-tech text-xs text-zinc-400 uppercase tracking-widest font-bold block">Feature Vectorization</span>
                    <span class="mono-tech text-[10px] text-zinc-600">User \xd7 Movie Tensor \u2014 FLOAT32</span>
                </div>
                <span class="mono-tech text-[10px] text-emerald-400/80 border border-emerald-500/20 bg-emerald-500/5 px-2 py-0.5 rounded">LIVE</span>
            </div>

            <!-- Tensor Grid with Labels -->
            <div class="border border-white/5 rounded-lg bg-black/40 p-4 font-mono text-xs">
                <div class="grid grid-cols-4 gap-2 w-full text-center" id="vectorization-grid">
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-yellow-400 font-bold text-[11px]">[0.50]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Action</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-yellow-400 font-bold text-[11px]">[0.50]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Sci-Fi</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-yellow-400 font-bold text-[11px]">[0.50]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Drama</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-yellow-400 font-bold text-[11px]">[0.50]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Comedy</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-yellow-400 font-bold text-[11px]">[0.50]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Horror</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-yellow-400 font-bold text-[11px]">[0.50]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Thriller</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-yellow-400 font-bold text-[11px]">[0.50]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Romance</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-yellow-400 font-bold text-[11px]">[0.50]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Fantasy</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-cyan-400 font-bold text-[11px]">[0.65]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Age</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-cyan-400 font-bold text-[11px]">[0.80]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Watch Hist</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-cyan-400 font-bold text-[11px]">[0.72]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Avg Rating</span></div>
                    <div class="flex flex-col gap-1 group"><div class="vec-cell bg-white/5 p-2 rounded border border-white/5 transition-all duration-300 text-cyan-400 font-bold text-[11px]">[0.91]</div><span class="mono-tech text-[8px] text-zinc-600 uppercase group-hover:text-zinc-400 transition-colors">Pop Score</span></div>
                </div>

                <!-- Heatmap Legend -->
                <div class="mt-4 pt-3 border-t border-white/5">
                    <div class="flex items-center justify-between mb-1">
                        <span class="mono-tech text-[8px] text-zinc-600 uppercase">Activation Strength</span>
                        <span class="mono-tech text-[8px] text-zinc-600">x' = x / 100</span>
                    </div>
                    <div class="w-full h-1.5 rounded-full overflow-hidden" style="background: linear-gradient(to right, #1e293b, #b45309, #facc15, #4ade80)"></div>
                    <div class="flex justify-between mt-1">
                        <span class="mono-tech text-[8px] text-zinc-700">0.00 Low</span>
                        <span class="mono-tech text-[8px] text-zinc-700">1.00 High</span>
                    </div>
                </div>
            </div>

            <!-- Annotation box -->
            <div class="bg-indigo-950/30 border border-indigo-500/10 rounded-lg p-3">
                <p class="mono-tech text-[9px] text-zinc-500 leading-relaxed">
                    <span class="text-indigo-400 font-bold">HOW IT WORKS:</span> Each slider value (0\u2013100) is normalized to [0,1] using <span class="text-cyan-400">x' = x / 100</span>. These 12 values form the <span class="text-violet-400">input layer tensor</span> fed into the first neural network layer. Values update live as you adjust genre preferences.
                </p>
            </div>
        </div>`;

if (html.includes(oldSection)) {
    html = html.replace(oldSection, newSection);
    fs.writeFileSync(file, html);
    console.log('Done: Input Vectorization enhanced successfully.');
} else {
    // Fuzzy fallback – find by landmark
    const startMarker = '<!-- Input Image Viz -->';
    const endMarker = '</div>\n    </div>';
    const startIdx = html.indexOf(startMarker);
    if (startIdx === -1) { console.log('ERROR: marker not found'); process.exit(1); }
    // Find 3 closing divs after startIdx
    let closeCount = 0;
    let i = startIdx;
    while (i < html.length && closeCount < 3) {
        if (html.substring(i, i+6) === '</div>') closeCount++;
        i++;
    }
    const endIdx = i + 5; // include last </div>
    html = html.substring(0, startIdx) + newSection + html.substring(endIdx);
    fs.writeFileSync(file, html);
    console.log('Done (fuzzy match): Input Vectorization enhanced successfully.');
}
