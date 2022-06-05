const path = require('path');
const fs = require('fs');
const { JSDOM } = require('jsdom');

async function main() {
    const figDir = "docs/figs";
    const latestFigDir = `${figDir}/latest`;
    const templateHtml = "docs/template.html";
    const resultHtml = "docs/index.html";

    const DOM = await JSDOM.fromFile(templateHtml);
    const { document } = DOM.window;
    const parentDiv = document.getElementById("main_images");

    // create explanation
    let textHeaderDiv = document.createElement("h1");
    textHeaderDiv.id = "textHeaderImg";
    textHeaderDiv.append("コンテンツ一覧");
    parentDiv.appendChild(textHeaderDiv);

    const latestFileName = fs.readdirSync(latestFigDir)[0];
    let resLatestImg = document.createElement("img");
    resLatestImg.src = `figs/latest/${latestFileName}`;
    resLatestImg.alt = latestFileName;
    parentDiv.appendChild(document.createElement("div").appendChild(resLatestImg));

    //create img list in latest to oldest order
    const fileNames = fs.readdirSync(figDir, {withFileTypes: true})
        .filter(d => !d.isDirectory())
        .map(d => d.name)
        .sort()
        .reverse();

    fileNames.forEach(fileName => {
        let resDiv = document.createElement("div")
        let resImg = document.createElement("img")
        resImg.src = `figs/${fileName}`;
        resImg.alt = fileName;
        resDiv.appendChild(resImg);
        parentDiv.appendChild(resDiv);
    })

    console.log(document.documentElement.outerHTML);
    fs.writeFileSync(resultHtml, document.documentElement.outerHTML);

}

main();