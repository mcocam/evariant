/* SNP results request results page js
@author: Melania Prado */

$().ready(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const fasta_id = urlParams.get('fasta_id');

  axios.get('/api/snp/results/' + fasta_id)
    .then(function (response) {
      const snpRefs = response.data[0].snp_references;
      const snpGenotypes = response.data[1].snp_genotypes;

      const snpRelatedArticles = response.data[1].snp_articles;
      const snpArticlesURL = response.data[1].snp_articles_url;
      const articlesTitles = response.data[1].snp_articles_titles;

      const snpRegions = response.data[1].snp_regions;

      const accordionContainer = $('#accordion');

      // Iterate over each SNP key in the response
      snpRefs.forEach(function (snpRef) {
        const snpValues = snpGenotypes[snpRef];

        // Create the accordion for the current SNP
        const accordion = $('<div>').addClass('accordion').attr('id', `${snpRef}-accordion`);
        accordionContainer.append(accordion);



        // GENOTYPES ============================================================================================================================================================


        //Genotype Comparative Card
        const genotypeCard = $('<div>').addClass('card snp-result-card');
        const genotypeCardHeader = $('<div>').addClass('card-header d-flex');
        const genotypeCardContent = $('<div>').addClass('collapse show').attr('id', `${snpRef}-genotype-collapse`);
        const genotypeCardBody = $('<div>').addClass('card-body');

        // Add the SNP reference and genotype to the genotype card header
        const snpRefText = $('<span>').addClass('snp-ref').text(snpRef);
        const genotype = snpValues[0];
        const genotypeText = $('<span>').addClass('me-3').text(`Genotype ${genotype}`);
        genotypeCardHeader.append(snpRefText, genotypeText);

        // Add the genotype card header and content to the genotype card
        genotypeCard.append(genotypeCardHeader, genotypeCardContent);

        // Add the genotype card to the accordion
        accordion.append(genotypeCard);

        // Genotype Comparative Table
        const genotypeTable = $('<table>').addClass('table');
        const genotypeTableHead = $('<thead>');
        const genotypeTableBody = $('<tbody>');

        // Create table header
        const genotypeTableHeaderRow = $('<tr>');
        const genotypeHeader = $('<th>').attr('scope', 'col').text('Genotype');
        const magnitudeHeader = $('<th>').attr('scope', 'col').text('Magnitude');
        const summaryHeader = $('<th>').attr('scope', 'col').text('Summary');
        genotypeTableHeaderRow.append(genotypeHeader, magnitudeHeader, summaryHeader);
        genotypeTableHead.append(genotypeTableHeaderRow);

        // Create table rows for each SNP genotype
        for (let i = 0; i < snpValues.length; i += 3) {
          const snpGenotype = snpValues[i];
          const magnitude = snpValues[i + 1];
          const summary = snpValues[i + 2];

          const tableRow = $('<tr>');
          const genotypeCell = $('<td>').addClass('genotype').text(snpGenotype);
          const magnitudeCell = $('<td>').text(magnitude);
          const summaryCell = $('<td>').text(summary);
          tableRow.append(genotypeCell, magnitudeCell, summaryCell);
          genotypeTableBody.append(tableRow);
        }

        // Add the genotype table to the genotype card body
        genotypeCardBody.append(genotypeTable.append(genotypeTableHead, genotypeTableBody));

        // Add the genotype card body to the genotype card content
        genotypeCardContent.append(genotypeCardBody);



        // RELATED ARTICLES ====================================================================================================================================================
        // Related Articles Card
        const articlesCard = $('<div>').addClass('card snp-result-card');
        const articlesCardHeader = $('<div>').addClass('card-header d-flex');
        const articlesCardContent = $('<div>').addClass('collapse show').attr('id', `${snpRef}-articles-collapse`);
        const articlesCardBody = $('<div>').addClass('card-body');

        // Add the related articles card header
        const articlesHeader = $('<h5>', { class: 'mb-0', text: 'Related Articles' });
        articlesCardHeader.append(articlesHeader);

        // Add the articles card header and content to the articles card
        articlesCard.append(articlesCardHeader, articlesCardContent);

        // Add the articles card to the accordion
        accordion.append(articlesCard);

        // Related Articles Table
        const articlesTable = $('<table>', { class: 'table' });
        const articlesTableHead = $('<thead>');
        const articlesTableBody = $('<tbody>');

        // Create table header
        const articlesTableHeaderRow = $('<tr>');
        const articlePMIDHeader = $('<th>').attr('scope', 'col').text('PMID');
        const articleTitleHeader = $('<th>').attr('scope', 'col').text('Title');
        articlesTableHeaderRow.append(articlePMIDHeader, articleTitleHeader);
        articlesTableHead.append(articlesTableHeaderRow);


        // Create table rows for each related article of the current SNP
        const articleArray = snpRelatedArticles[snpRef];
        const articleTitleText = articlesTitles[snpRef]; // Use snpRef as the key to access the title

        if (articleArray && articleArray.length > 0) {
          articleArray.forEach(function (article, index) {
            const tableRow = $('<tr>');
            const articlePMIDCell = $('<td>').addClass('article-PMID').text(article);
            const articleTitleCell = $('<td>').addClass('article-title').text(articleTitleText[index]);
            tableRow.append(articlePMIDCell, articleTitleCell);
            articlesTableBody.append(tableRow);

            // Add click event listener to open related article URL in a new tab
            tableRow.on('click', function () {
              window.open(snpArticlesURL[article], '_blank');
            });
          });
        } else {
          const noArticlesMessage = $('<tr>').append($('<td>').attr('colspan', '2').text('No related articles found.'));
          articlesTableBody.append(noArticlesMessage);
        }

        // Add the articles table to the articles card body
        articlesCardBody.append(articlesTable.append(articlesTableHead, articlesTableBody));

        // Add the articles card body to the articles card content
        articlesCardContent.append(articlesCardBody);

      });

      // Add event listener to collapse/expand accordion
    })
    .catch(function (error) {
      console.log(error.stack);
    });
});