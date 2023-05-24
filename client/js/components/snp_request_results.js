$().ready(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const fasta_id = urlParams.get('fasta_id');

  axios.get('/api/snp/results/' + fasta_id)
    .then(function (response) {

      // Extract response data
      const snpRefs = response.data.snp_refs;
      const snp_ref_nucleotides = response.data.snp_ref_nucleotides
      const snp_var_nucleotides = response.data.snp_var_nucleotides
      const snpGenotypes = response.data.snp_genotypes;
      const snpRelatedArticles = response.data.snp_articles;
      const snpArticlesURL = response.data.snp_articles_url;
      const articlesTitles = response.data.snp_articles_titles;
      //const regionsValues = response.data.snp_regions_values;
      //const regionsDesc = response.data.snp_regions_desc;

      // Define outer structure for data
      const resultsContainer = $('#results_body');

      // Iterate over each SNP key in the response
      if (Array.isArray(snpRefs)) {
        if (snpRefs.length > 0) {

          // Iterate found snp and display results and related data
          snpRefs.forEach(function (snpRef, index) {

            // Create the accordion for the current SNP
            const accordion = $('<div>').addClass('accordion mt-5').attr('id', `${snpRef}-accordion`);
            const accordionContent = $('<div>').addClass('accordion-content').attr('id', `${snpRef}-accordion-content`);
            const accordionHeader = $('<div>').addClass('d-flex justify-content-between align-items-center');


            // Build found SNP and nucleotides info

            const snpRefText = $('<span>').addClass('snp-ref').text(`SNP: ${snpRef}`);
            const snp_ref_nucleotide = snp_ref_nucleotides[index];
            const snp_var_nucleotide = snp_var_nucleotides[index];
            const refNucleotideText = $('<span>').addClass('me-3').text(`Ref nucleotide ${snp_ref_nucleotide}`);
            const varNucleotideText = $('<span>').addClass('me-3').text(`Found nucleotide ${snp_var_nucleotide}`);
            accordionHeader.append(snpRefText, refNucleotideText, varNucleotideText);


            // Build SNP genotypes info

            let genotypeCard = '';
            const snpGenotypeData = snpGenotypes[index];
            let genotype = [];
            console.log(snpGenotypeData[1]);
            if (typeof snpGenotypeData[1] !== undefined) {
              if (snpGenotypeData[1] !== '') {

                //Genotype Comparative Card
                genotypeCard = $('<div>').addClass('card snp-result-card mt-4');
                const genotypeCardHeader = $('<div>').addClass('card-header d-flex').attr('id', `${snpRef}-genotype-card-header`);
                const genotypeCardContent = $('<div>').addClass('card-content');
                const genotypeCardBody = $('<div>').addClass('card-body');

                // Add the SNP reference and genotype to the genotype card header
                const genotypeHeader = $('<h5>', { class: 'mb-0' });
                const collapseBtn = $('<button>').addClass('btn btn-link card-header-text').text('Genotype comparative').attr('href', `#genotype-collapse-${snpRef}`).attr('data-bs-toggle', 'collapse').attr('data-bs-target', `#genotype-collapse-${snpRef}`).attr('aria-expanded', 'true').attr('aria-controls', `genotype-collapse-${snpRef}`);
                genotypeHeader.append(collapseBtn);
                const genotypeCollapseDiv = $('<div>').addClass('collapse').attr('id', `genotype-collapse-${snpRef}`).attr('aria-labelledby', `${snpRef}-genotype-card-header`).attr('data-bs-parent', 'accordionContent');

                genotypeCardHeader.append(genotypeHeader, collapseBtn);

                genotype = snpGenotypeData[1];

                // Genotype Comparative Table
                const genotypeTable = $('<table>').addClass('table');
                const genotypeTableHead = $('<thead>');
                const genotypeTableBody = $('<tbody>');

                // Create table header
                const genotypeTableHeaderRow = $('<tr>');
                const genotypeTableHeader = $('<th>').attr('scope', 'col').text('Genotype');
                const magnitudeHeader = $('<th>').attr('scope', 'col').text('Magnitude');
                const summaryHeader = $('<th>').attr('scope', 'col').text('Summary');
                genotypeTableHeaderRow.append(genotypeTableHeader, magnitudeHeader, summaryHeader);
                genotypeTableHead.append(genotypeTableHeaderRow);

                const genotypesList = [];
                // Create table rows for each SNP genotype
                for (let i = 0; i < genotype.length; i += 3) {
                  const snpGenotype = genotype[i];
                  genotypesList.push(snpGenotype);
                  const magnitude = genotype[i + 1];
                  const summary = genotype[i + 2];

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
                genotypeCollapseDiv.append(genotypeCardContent);
                genotypeCard.append(genotypeCardHeader, genotypeCollapseDiv);

                genotypeCard.append(genotypeCardContent);
              } else {
                const noGenotypeDatafound = $('<h4>').addClass('m-5 info-message').text('There are no Genotypes Data available or reachable for this SNP.').attr('id', 'no-genotype-data-message');
                resultsContainer.append(noGenotypeDatafound);
              }
            } else {
              const noGenotypeDatafound = $('<h4>').addClass('m-5 info-message').text('There are no Genotypes Data available or reachable for this SNP.').attr('id', 'no-genotype-data-message');
              resultsContainer.append(noGenotypeDatafound);
            }


            let articlesCard = '';
            // Create table rows for each related article of the current SNP
            const articlesArray = snpRelatedArticles[index];

            let articles = [];
            if (typeof articlesArray[1] !== undefined) {
              if (articlesArray[1] !== '') {

                // Build SNP related articles info
                // Related Articles Card
                articlesCard = $('<div>').addClass('card snp-result-card mt-4');
                const articlesCardHeader = $('<div>').addClass('card-header d-flex');
                const articlesCardContent = $('<div>').addClass('collapse show').attr('id', `${snpRef}-articles-collapse`);
                const articlesCardBody = $('<div>').addClass('card-body');

                // Add the related articles card header
                const articlesHeader = $('<h5>', { class: 'mb-0 card-header-text', text: 'Related Articles' });
                articlesCardHeader.append(articlesHeader);

                // Add the articles card header and content to the articles card
                articlesCard.append(articlesCardHeader, articlesCardContent);


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


                articles = articlesArray[1];
                const titlesArray = articlesTitles[index];
                const titles = titlesArray[1];
                const articlesURLarray = snpArticlesURL[index];
                const URLs = articlesURLarray[1]

                if (articles && articles.length > 0) {
                  articles.forEach(function (article, index) {
                    const tableRow = $('<tr>');
                    const articlePMIDCell = $('<td>').addClass('article-PMID');
                    const articlePMIDlink = $('<a>').text(article).attr('href', `${URLs[index]}`).attr('target', '_blank');
                    const articleTitleCell = $('<td>').addClass('article-title').text(titles[index]);
                    articlePMIDCell.append(articlePMIDlink);
                    tableRow.append(articlePMIDCell, articleTitleCell);
                    articlesTableBody.append(tableRow);

                  });
                } else {
                  const noArticlesMessage = $('<tr>').append($('<td>').attr('colspan', '2').text('No related articles found.'));
                  articlesTableBody.append(noArticlesMessage);
                }

                // Add the articles table to the articles card body
                articlesCardBody.append(articlesTable.append(articlesTableHead, articlesTableBody));

                // Add the articles card body to the articles card content
                articlesCardContent.append(articlesCardBody);

                articlesCard.append(articlesCardContent);
              } else {
                const noArticlesfound = $('<h4>').addClass('m-5 info-message').text('There are no articles available or reachable for this SNP.').attr('id', 'no-articles-data-message');
                resultsContainer.append(noArticlesfound);
              }
            } else {
              const noArticlesfound = $('<h4>').addClass('m-5 info-message').text('There are no articles available or reachable for this SNP.').attr('id', 'no-articles-data-message');
              resultsContainer.append(noArticlesfound);
            }

            accordionContent.append(accordionHeader, genotypeCard, articlesCard);
            accordion.append(accordionContent);
            resultsContainer.append(accordion);


          })
        } else {
          const noSNPfound = $('<h2>').addClass('m-5').text('There are no SNP found in this sequence.').attr('id', 'no-snp-message');
          resultsContainer.append(noSNPfound);
        }

      } else {
        console.error('snpRefs is not an array or is undefined');
      }
    })
    .catch(function (error) {
      console.log(error.stack);
    });
});