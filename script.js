//getting the list of words to redact that are saved in to_redact.txt
path = this.path
ind = path.indexOf('/') + 1
path_temp = path.substr(ind)
ind = ind + path_temp.indexOf('/') + 1
path_temp = path.substr(ind)
ind = ind + path_temp.indexOf('/') + 1
path_temp = path.substr(ind)
ind = ind + path_temp.indexOf('/') + 1
path_final = path.substr(0, ind) + 'Desktop/to_redact.csv'
var oFile = util.readFileIntoStream(path_final, 0);
var cFile = util.stringFromStream(oFile, "utf-8");
var censurar = cFile.split(/\r?\n|\r|\n/g)
censurar.shift()

function search_and_annot(term) {
    pos = term.lastIndexOf(",")
    page = term.substr(pos + 1, term.length)-1
    wordss = term.substr(0, pos)
    words = wordss.split([' '])
    
    if (words.length == 1) {
        var rg = new RegExp(word);
        var len = getPageNumWords(page)

        for (var i = 0; i < len; i++) {
            var wd = this.getPageNthWord(page, i, false)

            if (rg.test(wd)) {
                qd = getPageNthWordQuads(page, i)
                qd.toSource()

                this.addAnnot({
                    type: "Redact",
                    page: page,
                    quads: qd,
                    alignment: 1, // Center alignment
                    repeat: true
                })
            }
        }
    } else {
        var rg = new RegExp(words[0]);
        
        var len = getPageNumWords(page)

        for (var i = 0; i < len; i++) {
            var position = -1 //for saving the position of words[0]
            var wd = this.getPageNthWord(page, i, false)

            if (rg.test(wd)) {
                position = i

                var qd1 = getPageNthWordQuads(page, position)
                qd1 = String(qd1).split(',')

                rg2 = new RegExp(words[words.length - 1])  // for saving the posible words[-1] 
                wd2 = this.getPageNthWord(page, position + words.length - 1, false)
                if (rg2.test(wd2)) { // checks if rg2 trully is words[-1]
                    var qd2 = getPageNthWordQuads(page, position + words.length - 1)
                a    qd2 = String(qd2).split(',')

                    if (qd1[1] == qd2[1]) { //checks if words[0] is in the same line as words[-1]

                        // qd = [[left, top, right, top, left, bot, right, bot]];
                        var qd = [[qd1[0], qd1[1], qd2[2], qd1[3], qd1[4], qd1[5], qd2[6], qd1[7]]]

                        this.addAnnot({
                            type: "Redact",
                            page: page,
                            quads: qd,
                            alignment: 1,
                            repeat: true
                        })
                    } else {
                        for (var w = 0; w < words.length; w++) {
                            var qd = getPageNthWordQuads(page, position + w)

                            this.addAnnot({
                                type: "Redact",
                                page: page,
                                quads: qd,
                                alignment: 1,
                                repeat: true
                            })
                            current_page = page
                        }
                    }
                }
            }
        }
    }
}

for (var i = 0; i < censurar.length; i++) {
    search_and_annot(censurar[i])
}
