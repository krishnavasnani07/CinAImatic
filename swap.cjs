const fs = require('fs');

const file = 'c:\\Users\\Krishna\\Documents\\Movie recommendation system\\screens\\Neural_Network_Engine.html';
let html = fs.readFileSync(file, 'utf8');

// Extract graphs
const graphsRegex = /<!-- Cost Graph -->[\s\S]*?<!-- Accuracy Graph -->[\s\S]*?<\/canvas><\/div>\s*<\/div>/;
const graphsMatch = html.match(graphsRegex);
const graphsHTML = graphsMatch ? graphsMatch[0] : '';

// Extract genre section
const genreRegex = /<div class="space-y-6">\s*<div>\s*<p class="mono-tech text-\[11px\] text-zinc-500 uppercase tracking-wider mb-4">Core Genre Preference Strength<\/p>[\s\S]*?<\/details>\s*<\/div>\s*<\/div>/;
const genreMatch = html.match(genreRegex);
let genreHTML = genreMatch ? genreMatch[0] : '';

// Process Genre HTML for sidebar
// Update grid classes to be 1 or 2 columns instead of 4
genreHTML = genreHTML.replace(/grid-cols-1 sm:grid-cols-2 lg:grid-cols-4/g, 'grid-cols-1 xl:grid-cols-2');
// Add max-height and overflow to the main genre container if needed, but it's already in the left column which might scroll
genreHTML = genreHTML.replace('<div class="space-y-6">', '<div class="space-y-6 flex-1 overflow-y-auto custom-scrollbar pr-2 pb-4" style="max-height: 800px;">');
genreHTML = genreHTML.replace(/max-h-\[500px\] overflow-y-auto/g, ''); // remove inner scrollbar since outer will scroll

// Process Graphs HTML for main panel
let newGraphsHTML = `
<div class="space-y-6">
    <p class="mono-tech text-[11px] text-zinc-500 uppercase tracking-wider mb-4">Model Performance Metrics</p>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        ${graphsHTML}
    </div>
</div>
`;

// Replace in original HTML
html = html.replace(graphsRegex, genreHTML);
html = html.replace(genreRegex, newGraphsHTML);

fs.writeFileSync(file, html);
console.log('Swap completed.');
