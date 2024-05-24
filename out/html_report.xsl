<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <head>
    <title>Perco</title>
    <!-- CDN Bootstrap - CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous" />
    <!-- fichier style.css -->
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div classs="container">
      <h2 class="center">Fonds PERCO</h2>
    </div>
    <div class="container">
      <h3 class="my">Synthèse</h3>
      <table class="table table-striped  table-hover">
        <thead>
          <tr class="table-primary">
            <th scope="col" class="center">nom</th>
            <th scope="col" class="center">nb parts</th>
            <th scope="col" class="center">date</th>
            <th scope="col" class="center">valeur</th>
            <th scope="col" class="center">variation</th>
            <th scope="col" class="center">capitalisation</th>
          </tr>
        </thead>
        <tbody>
          <xsl:for-each select="wallet/fund">
            <tr>
              <td scope="row" class="center"><xsl:value-of select="./@name"/></td>
              <td class="right"><xsl:value-of select="./@parts"/></td>
              <td class="center"><xsl:value-of select="./@lcdate"/></td>
              <td class="right"><xsl:value-of select="./@lcval"/></td>
              <td class="right"><xsl:value-of select="./@lv"/></td>
              <td class="right"><xsl:value-of select="./@capital"/></td>
            </tr>
          </xsl:for-each>
        </tbody>
      </table>
    </div>
    <div class="container">
      <h3 class="my">Capitalisation</h3>
      <div class="alert alert-primary">
        Total = <b><xsl:value-of select="wallet/@capital"/></b>
      </div>
    </div>
    <div class="container">
      <h3 class="my">Histogramme</h3>
      <img src="01_suivi_fonds.png" />
      <img src="01_suivi_capital.png" />
      <img src="01_evol_fonds.png" />
      <img src="01_synthese_fonds.png" />
    </div>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
