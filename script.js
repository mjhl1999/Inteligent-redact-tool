var censurar = ['Mónica González Contró', 'UNAM', 'Edna Jaime', 'Arturo Zaldívar', 'Norma Piña', 'Alberto Pérez Dayán', 'Javier Laynez', 'Hugo Concha']


function search_and_annot(word) {
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

}


for (var i = 0; i < censurar.length; i++) {
  search_and_annot(censurar[i])
}


this.applyRedactions({
  bKeepMarks: false,
  bShowConfirmation: false,
})