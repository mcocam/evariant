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
      const regionsValues = response.data.snp_regions_values;
      const regionsDesc = response.data.snp_regions_desc;

      // Define outer structure for data
      const resultsContainer = $('#results_body');
      //const accordionContainer = $('#accordion');

      // Iterate over each SNP key in the response
      if (Array.isArray(snpRefs)) {
        if(snpRefs.length > 0) {

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

            //Genotype Comparative Card
            const genotypeCard = $('<div>').addClass('card snp-result-card mt-4');
            const genotypeCardHeader = $('<div>').addClass('card-header d-flex').attr('id', `${snpRef}-genotype-card-header`);
            const genotypeCardContent = $('<div>').addClass('card-content');
            const genotypeCardBody = $('<div>').addClass('card-body');

            // Add the SNP reference and genotype to the genotype card header
            const genotypeHeader = $('<h5>', { class: 'mb-0'});
            const collapseBtn = $('<button>').addClass('btn btn-link').text('Genotype comparative').attr('href', `#genotype-collapse-${snpRef}`).attr('data-bs-toggle', 'collapse').attr('data-bs-target', `#genotype-collapse-${snpRef}`).attr('aria-expanded', 'true').attr('aria-controls', `genotype-collapse-${snpRef}`);
            genotypeHeader.append(collapseBtn);
            const genotypeCollapseDiv = $('<div>').addClass('collapse').attr('id', `genotype-collapse-${snpRef}`).attr('aria-labelledby', `${snpRef}-genotype-card-header`).attr('data-bs-parent', 'accordionContent');

            genotypeCardHeader.append(genotypeHeader, collapseBtn);
            const snpGenotypeData = snpGenotypes[index];
            const genotype = snpGenotypeData[1];
        
            


            // Add the genotype card header and content to the genotype card
            //genotypeCard.append(genotypeCardHeader, genotypeCardContent);

            // Add the genotype card to the accordion
            //accordion.append(genotypeCard);

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



            // Build SNP related articles info RELATED ARTICLES
            // Related Articles Card
            const articlesCard = $('<div>').addClass('card snp-result-card mt-4');
            const articlesCardHeader = $('<div>').addClass('card-header d-flex');
            const articlesCardContent = $('<div>').addClass('collapse show').attr('id', `${snpRef}-articles-collapse`);
            const articlesCardBody = $('<div>').addClass('card-body');

            // Add the related articles card header
            const articlesHeader = $('<h5>', { class: 'mb-0', text: 'Related Articles' });
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


            // Create table rows for each related article of the current SNP
            const articlesArray = snpRelatedArticles[index];
            const articles = articlesArray[1]
            const titlesArray = articlesTitles[index]
            const titles = titlesArray[1]


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

            

            // POPULATION DIVERSITY ====================================================================================================================================================
            // Population Card
            const populationCard = $('<div>').addClass('card snp-result-card mt-4');
            const populationCardHeader = $('<div>').addClass('card-header d-flex');
            const populationCardContent = $('<div>').addClass('collapse show').attr('id', `${snpRef}-regions-collapse`);
            const populationCardBody = $('<div>').addClass('card-body');

            // Add the population diversity card header
            const populationHeader = $('<h5>', { class: 'mb-0', text: 'Population Diversity' });
            populationCardHeader.append(populationHeader);

            // Population Diversity Table
            const populationTable = $('<table>', { class: 'table' });
            const populationTableHead = $('<thead>');
            const populationTableBody = $('<tbody>');

            // Create table header
            const populationTableHeaderRow = $('<tr>');
            const regionHeader = $('<th>').attr('scope', 'col').text('Population');
            const regionDistHeader = $('<th>').attr('scope', 'col').text(`Distribution. ${genotypesList}`);
            populationTableHeaderRow.append(regionHeader, regionDistHeader);
            populationTableHead.append(populationTableHeaderRow);


            // Create table rows for each related article of the current SNP
            const regionsArray = regionsValues[index];
            const regionsVal = regionsArray[1]

            const regionsDescArray = regionsDesc[index];
            const regionsDe = regionsDescArray[1]



            // ======================================================================================================================================================== 

            // Append cards to snp accordion div and results container in results page
            genotypeCard.append(genotypeCardContent);
            articlesCard.append(articlesCardContent);
            populationCard.append(populationCardContent);
            accordionContent.append(accordionHeader,genotypeCard, articlesCard, populationCard);
            accordion.append(accordionContent);
            resultsContainer.append(accordion);


            if (regionsDe && regionsDe.length > 0) {
              regionsDe.forEach(function (region, index) {
                const tableRow = $('<tr>');
                const regionsDeCell = $('<td>').addClass('region-desc');
                const regionValuesCell = $('<td>').addClass('article-title').text(regionsVal[index]);
                tableRow.append(regionsDeCell, regionsValuesCell);
                populationTableBody.append(tableRow);

              });
            } else {
              const noPopulationsMessage = $('<tr>').append($('<td>').attr('colspan', '2').text('No populations info found.'));
              populationTableBody.append(noPopulationsMessage);
            }

            // Add the population distribution table to the articles card body
            populationCardBody.append(populationTable.append(populationTableHead, populationTableBody));

            // Add the population distribution card body to the articles card content
            populationCardContent.append(populationCardBody);


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