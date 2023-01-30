var censurar = ['Mónica González Contró', 'UNAM', 'México Evalúa', 'Edna Jaime', 'Ministro Arturo Zaldívar', 'Ministra Norma Piña', 'Ministro Alberto Pérez Dayán', 'Javier Laynez', 'Hugo Concha']


function search_and_annot(word) {
  words = word.split([' '])
  if (words.length == 1){
    var rg = new RegExp(word);

    for (var pg = 0; pg < this.numPages; pg++) {
      var len = getPageNumWords(pageNum)

      for (var i = 0; i < len; i++) {
        var wd = this.getPageNthWord(pg, i, false)

        if (rg.test(wd)) {
          qd = getPageNthWordQuads(pg, i)
          qd.toSource()

          this.addAnnot({
            type: "Redact",
            page: 0,
            quads: qd,
            alignment: 1, // Center alignment
            repeat: true
          })
        }
      }
    }
  }else{
    var rg = new RegExp(words[0]);
    
    for (var pg = 0; pg < this.numPages; pg++) {
      var len = getPageNumWords(pageNum)
      
      for (var i = 0; i < len; i++) {
        var position = -1 //for saving the position of words[0]
        var wd = this.getPageNthWord(pg, i, false)

        if (rg.test(wd)) {
          position = i 

          var qd1 = getPageNthWordQuads(pg, position)
          qd1 = String(qd1).split(',')
          
          rg2 = new RegExp(words[words.length-1])  // for saving the posible words[-1] 
          wd2 = this.getPageNthWord(pg, position+words.length-1, false)
          if (rg2.test(wd2)){ // checks if rg2 trully is words[-1]
            var qd2 = getPageNthWordQuads(pg, position+words.length-1)
            qd2 = String(qd2).split(',')

            if (qd1[1] == qd2[1]) { //checks if words[0] is in the same line as words[-1]

              // qd = [[left, top, right, top, left, bot, right, bot]];
              var qd = [[qd1[0], qd1[1], qd2[2], qd1[3], qd1[4], qd1[5], qd2[6], qd1[7]]] 
              
              this.addAnnot({
                type: "Redact",
                page: 0,
                quads: qd,
                alignment: 1, 
                repeat: true
              })
            }else{ 
              var position2 = -1; // for saving the last word in the same line as words[0]
              for (var w=0; w < words.length-1; w++){
                var qdw = getPageNthWordQuads(pg, position + w)
                qdw = String(qdw).split(',')
                if (qd1[1] == qdw[1]){
                  continue
                }else{
                  if (w == 0){
                    position2 = position
                  }else{
                    position2 = position + w - 1
                  }
                }
              }

              if (position2 == position){
                qd1_r1 = qd1
              }else{
                qd1_fin = getPageNthWordQuads(pg, position2)
                qd1_fin = String(qd1_fin).split(',')
                var qd_r1 = [[qd1[0], qd1[1], qd1_fin[2], qd1[3], qd1[4], qd1[5], qd1_fin[6], qd1[7]]] 
              }

              this.addAnnot({
                type: "Redact",
                page: 0,
                quads: qd_r1,
                alignment: 1,
                repeat: true
              })

              qd2_inicio = getPageNthWordQuads(pg, position2+1)
              qd2_inicio = String(qd2_inicio).split(',')

              var qd_r2 = [[qd2_inicio[0], qd2_inicio[1], qd2[2], qd2_inicio[3], qd2_inicio[4], qd2_inicio[5], qd2[6], qd2_inicio[7]]] 

              this.addAnnot({
                type: "Redact",
                page: 0,
                quads: qd_r2,
                alignment: 1,
                repeat: true
              })

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

this.applyRedactions({
  bKeepMarks: false,
  bShowConfirmation: false,
})
