const request = require("request");
const { JSDOM } = require("jsdom");
const fs = require("fs");
const { exit } = require("process");

let songList = [];

request("https://pjsekai.com/?aad6ee23b0", (e, res, body) => {
  if (e) {
    console.error(e);
  }

  const dom = new JSDOM(body);
  const tableData =
    dom.window.document.querySelector("#sortable_table1").tBodies[0];
  //   console.log(tableData);
  //   console.log(tableData.tBodies);
  //   console.log(tableData.tBodies[0]);
  //   console.log(tableData.tBodies[0].rows[0]);
  //   console.log(tableData.tBodies[0].rows[0].cells[0]);
  //   console.log(tableData.tBodies[0].rows[0].cells[1].innerHTML);

  for (const row of tableData.rows) {
    let songListRow = [];
    for (const cell of row.cells) {
      if (cell.childElementCount == 1) {
        // Hello,World is replaced to Hello World here
        songListRow.push(cell.children[0].innerHTML.replaceAll(",", " "));
      } else if (cell.childElementCount > 1) {
        console.log(`ERROR: cell has ${cell.childElementCount} elements`);
        exit(1);
      } else {
        songListRow.push(cell.innerHTML.replaceAll(",", " "));
      }
    }
    songList.push(songListRow);
  }

  console.log(...songList[0]);

  //   songList.splice(3);
  const resString = songList.reduce((acc, cur) => {
    acc += cur.join(",") + "\n";
    return acc;
  }, "");

  fs.writeFileSync("20220514_data.csv", resString);
});

// request("http://www.uec.ac.jp/", (e, response, body) => {
//   if (e) {
//     console.error(e);
//   }

//   try {
//     const dom = new JSDOM(body);
//     const latestDate = dom.window.document
//       .querySelector(".newsList")
//       .children[0].firstChild.textContent.trim();
//     console.log(`最新の新着情報の日付は${latestDate}です。`);
//   } catch (e) {
//     console.error(e);
//   }
// });
