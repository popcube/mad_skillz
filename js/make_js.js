const path = require('path');
const fs = require('fs');
const { JSDOM } = require('jsdom');

async function main() {
    const figDir = "docs/figs";
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

    //create img list in latest to oldest order
    const fileNames = fs.readdirSync(figDir).sort().reverse();

    fileNames.forEach(fileName => {
        let resImg = document.createElement("img")
        resImg.src = `${figDir.split("/")[1]}/${fileName}`;
        resImg.alt = fileName;
        parentDiv.appendChild(resImg);
    })

    console.log(document.documentElement.outerHTML);
    fs.writeFileSync(resultHtml, document.documentElement.outerHTML);

}

main();