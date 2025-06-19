// static/js/script.js

$(document).ready(function () {
    // Helper function to display Bootstrap alerts
    function displayErrorAlert(message, containerSelector) {
      const alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show mt-3" role="alert">
          <strong>Error:</strong> ${message}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
      $(containerSelector).html(alertHtml);
    }

    // Helper to manage button loading state
    function setLoadingState(buttonElement, isLoading) {
        const spinner = buttonElement.find('.spinner-border');
        const icon = buttonElement.find('.original-icon');

        if (isLoading) {
            buttonElement.prop('disabled', true);
            spinner.removeClass('d-none');
            if (icon.length) {
                icon.addClass('d-none');
            }
        } else {
            buttonElement.prop('disabled', false);
            spinner.addClass('d-none');
            if (icon.length) {
                icon.removeClass('d-none');
            }
        }
    }

    // Clear input/textarea fields
    $('.btn-clear').on('click', function() {
        const targetId = $(this).data('target');
        $(targetId).val('').focus();
         if (targetId === '#fileInput') {
            $('#fileNameDisplay').text('');
        }
    });

    // Display selected filename for file input
    $('#fileInput').on('change', function() {
        const fileName = $(this).val().split('\\').pop();
        if (fileName) {
            $('#fileNameDisplay').text(`Selected file: ${fileName}`);
        } else {
            $('#fileNameDisplay').text('');
        }
    });

    // --- AJAX Form Handlers ---
    $("#generateForm").on("submit", function (e) {
      e.preventDefault();
      $('#generateAlerts').empty();
      $('#generateResults').empty();
      const message = $("#message").val();
      const key = $("#key").val();
      const $button = $('#generateMacButton');
      setLoadingState($button, true);
      $.ajax({
        url: "/generate_mac",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ message: message, key: key }),
        success: function (response) {
          displayGenerateResults(response); // Panggil versi carousel
        },
        error: function (xhr) {
          const errorMsg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "An unknown error occurred.";
          displayErrorAlert(errorMsg, "#generateAlerts");
        },
        complete: function () {
          setLoadingState($button, false);
        }
      });
    });

    $("#verifyForm").on("submit", function (e) {
      e.preventDefault();
      $('#verifyAlerts').empty();
      $('#verifyResults').empty();
      const $button = $('#verifyMacButton');
      const data = {
        message: $("#verifyMessage").val(),
        key: $("#verifyKey").val(),
        mac_value: $("#macValue").val(),
        mac_type: $("#macType").val(),
        hash_algorithm: $("#hashAlgorithm").val(),
      };
      setLoadingState($button, true);
      $.ajax({
        url: "/verify_mac",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
          displayVerifyResults(response);
        },
        error: function (xhr) {
          const errorMsg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "An unknown error occurred.";
          displayErrorAlert(errorMsg, "#verifyAlerts");
        },
        complete: function() {
            setLoadingState($button, false);
        }
      });
    });

    $("#fileForm").on("submit", function (e) {
      e.preventDefault();
      $('#fileAlerts').empty();
      $('#fileResults').empty();
      const $button = $('#fileIntegrityButton');
      const formData = new FormData();
      const fileInput = $("#fileInput")[0];
      if (fileInput.files.length === 0) {
        displayErrorAlert("Please select a file.", "#fileAlerts");
        return;
      }
      if (fileInput.files[0].size > 10 * 1024 * 1024) {
          displayErrorAlert("File size exceeds 10MB limit.", "#fileAlerts");
          return;
      }
      formData.append("file", fileInput.files[0]);
      formData.append("key", $("#fileKey").val());
      setLoadingState($button, true);
      $.ajax({
        url: "/file_integrity",
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
          displayFileResults(response);
        },
        error: function (xhr) {
          const errorMsg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "An unknown error occurred.";
          displayErrorAlert(errorMsg, "#fileAlerts");
        },
        complete: function() {
            setLoadingState($button, false);
        }
      });
    });

    $("#loadComparison").on("click", function () {
  $('#compareAlerts').empty();
  $('#comparisonResults').empty();
  const $button = $(this);
  
  // Sembunyikan tombol dan tampilkan loader
  $button.hide();
  $('#compareLoader').removeClass('d-none');
  
  $.ajax({
    url: "/compare_algorithms",
    method: "GET",
    success: function (response) {
      displayComparisonResults(response);
    },
    error: function (xhr) {
      const errorMsg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "Failed to load algorithm comparison.";
      displayErrorAlert(errorMsg, "#compareAlerts");
    },
    complete: function() {
      // Sembunyikan loader dan tampilkan kembali tombolnya
      $('#compareLoader').addClass('d-none');
      $button.show();
    }
  });
});

    $("#fileHashForm").on("submit", function (e) {
        e.preventDefault();
        $('#fileHashAlerts').empty();
        $('#fileHashResults').empty();
        const $button = $('#fileHashButton');
        const formData = new FormData();
        const fileInput = $("#fileHashInput")[0];
        
        if (fileInput.files.length === 0) {
            displayErrorAlert("Please select a file.", "#fileHashAlerts");
            return;
        }
        if (fileInput.files[0].size > 10 * 1024 * 1024) {
            displayErrorAlert("File size exceeds 10MB limit.", "#fileHashAlerts");
            return;
        }
        formData.append("file", fileInput.files[0]);
        setLoadingState($button, true);
        
        $.ajax({
            url: "/file_hash_all_types",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                displayFileHashResults(response);
            },
            error: function (xhr) {
                const errorMsg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "An unknown error occurred.";
                displayErrorAlert(errorMsg, "#fileHashAlerts");
            },
            complete: function() {
                setLoadingState($button, false);
            }
        });
    });

    // BARU: Handler untuk form verifikasi file hash
    $("#verifyFileHashForm").on("submit", function (e) {
        e.preventDefault();
        $('#verifyFileHashAlerts').empty();
        $('#verifyFileHashResults').empty();
        const $button = $('#verifyFileHashButton');
        const formData = new FormData();
        const fileInput = $("#verifyFileHashInput")[0];
        
        if (fileInput.files.length === 0) {
            displayErrorAlert("Please select a file.", "#verifyFileHashAlerts");
            return;
        }
        
        formData.append("file", fileInput.files[0]);
        formData.append("hash_value", $("#hashValueToVerify").val());
        formData.append("algorithm", $("#hashAlgorithmVerify").val());
        
        setLoadingState($button, true);

        $.ajax({
            url: "/verify_file_hash_all_types",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                displayVerifyFileHashResults(response);
            },
            error: function (xhr) {
                const errorMsg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "An unknown error occurred.";
                displayErrorAlert(errorMsg, "#verifyFileHashAlerts");
            },
            complete: function() {
                setLoadingState($button, false);
            }
        });
    });

    // BARU: Fungsi untuk menampilkan hasil generate file hash
    function displayFileHashResults(response) {
        let fileSizeKB = (response.file_size / 1024).toFixed(2);
        let resultsHtml = `
            <div class="card result-card shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0"><i class="fas fa-file-invoice me-2"></i>File Hash Results</h5>
                </div>
                <div class="card-body p-4">
                    <p><strong>File:</strong> ${response.filename} (${fileSizeKB} KB)</p>
                    <hr>`;
        
        const hashes = Object.entries(response.hashes);
        hashes.forEach(([algorithm, hash]) => {
            resultsHtml += `
                <div class="method-item mb-3">
                    <small class="text-muted method-name d-block mb-1">${algorithm}</small>
                    <div class="hash-output p-2">${hash}</div>
                </div>`;
        });
        
        resultsHtml += `</div></div>`;
       const animatedHtml = `<div class="animate__animated animate__fadeInUp">${resultsHtml}</div>`;
    $("#fileHashResults").html(animatedHtml);
    }

    // BARU: Fungsi untuk menampilkan hasil verifikasi file hash
    function displayVerifyFileHashResults(response) {
        const isValid = response.is_valid;
        const cardClass = isValid ? "border-success" : "border-danger";
        const icon = isValid ? "fas fa-check-circle text-success" : "fas fa-times-circle text-danger";
        const status = isValid ? "VALID" : "INVALID";
        const statusText = isValid ? "The file hash matches the provided hash." : "The file hash does NOT match the provided hash.";

        const resultsHtml = `
            <div class="card result-card shadow-sm ${cardClass}">
                <div class="card-header">
                    <h5 class="mb-0"><i class="${icon} me-2"></i>Verification Result: HASH IS ${status}</h5>
                </div>
                <div class="card-body p-3">
                    <p class="mb-2">${statusText}</p>
                    <p class="mb-1"><strong>Calculated Hash (${response.algorithm}):</strong></p>
                    <div class="hash-output p-2">${response.calculated_hash}</div>
                    <p class="mt-3 mb-1"><strong>Provided Hash:</strong></p>
                    <div class="hash-output p-2">${response.provided_hash}</div>
                    <p class="mt-3 mb-0">
                        <small class="text-muted">File: ${response.filename}</small>
                    </p>
                </div>
            </div>`;
        const animatedHtml = `<div class="animate__animated animate__fadeInUp">${resultsHtml}</div>`;
    $("#verifyFileHashResults").html(animatedHtml);
    }

    // --- Display Functions (semua pada scope yang sama) ---

    // Versi Carousel untuk Hasil Generate MAC
    function displayGenerateResults(response) {
      const resultsContainer = $("#generateResults");
      resultsContainer.empty();

      const algorithms = Object.entries(response.results);

      if (algorithms.length === 0) {
        resultsContainer.html(`<div class="card result-card shadow-sm"><div class="card-body text-center text-muted p-4">No MACs generated.</div></div>`);
        return;
      }

      const carouselId = "macResultsCarousel_" + new Date().getTime();
      let carouselIndicatorsHtml = '';
      let carouselInnerHtml = '';

      algorithms.forEach(([algorithm, methods], index) => {
        carouselIndicatorsHtml += `
          <button type="button" data-bs-target="#${carouselId}" data-bs-slide-to="${index}" class="${index === 0 ? 'active' : ''}" aria-current="${index === 0 ? 'true' : 'false'}" aria-label="Slide ${index + 1} for ${algorithm}"></button>
        `;

        let methodsHtml = '<div class="methods-list p-3">';
        for (const [method, mac] of Object.entries(methods)) {
          methodsHtml += `
            <div class="method-item mb-3">
              <small class="text-muted method-name d-block mb-1">${method.replace(/_/g, " ").toUpperCase()}</small>
              <div class="hash-output p-2">${mac}</div>
            </div>`;
        }
        methodsHtml += '</div>';

        carouselInnerHtml += `
          <div class="carousel-item ${index === 0 ? 'active' : ''}">
            <div class="algorithm-slide-content">
              <h6 class="algorithm-title text-center my-3">
                <span class="badge bg-dark algorithm-badge px-3 py-2">${algorithm.toUpperCase()}</span>
              </h6>
              ${methodsHtml}
            </div>
          </div>
        `;
      });

      const fullCarouselHtml = `
         <div class="card result-card carousel-generate shadow-sm">
          <div class="card-header bg-light border-bottom d-flex justify-content-between align-items-center">
            <h5 class="mb-0"><i class="fas fa-key me-2"></i>Generated MACs</h5>
            <div class="carousel-indicators-container">
                <div class="carousel-indicators m-0 p-0">
                    ${carouselIndicatorsHtml}
                </div>
            </div>
          </div>
          <div class="card-body p-0">
            <div id="${carouselId}" class="carousel slide" data-bs-ride="carousel" data-bs-interval="false">
              <div class="carousel-inner">
                ${carouselInnerHtml}
              </div>
              <button class="carousel-control-prev" type="button" data-bs-target="#${carouselId}" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous Algorithm</span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#${carouselId}" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next Algorithm</span>
              </button>
            </div>
          </div>
        </div>
      `;
      const animatedHtml = `<div class="animate__animated animate__fadeInLeft">${fullCarouselHtml}</div>`;
  resultsContainer.html(animatedHtml);
}// Akhir dari displayGenerateResults (versi carousel)


    function displayVerifyResults(response) {
      const isValid = response.is_valid;
      // Gunakan kelas CSS dari file style.css untuk border-success/danger pada .result-card
      const cardClass = isValid ? "border-success" : "border-danger";
      const icon = isValid ? "fas fa-check-circle text-success" : "fas fa-times-circle text-danger";
      const status = isValid ? "VALID" : "INVALID";

      const resultsHtml = `
        <div class="card result-card shadow-sm ${cardClass}">
          <div class="card-header"> <!-- Header akan diwarnai oleh CSS berdasarkan ${cardClass} -->
            <h5 class="mb-0"><i class="${icon} me-2"></i>Verification Result: ${status}</h5>
          </div>
          <div class="card-body p-3">
            <p class="mb-1"><strong>Calculated MAC:</strong></p>
            <div class="hash-output p-2">${response.calculated_mac}</div>
            <p class="mt-3 mb-1"><strong>Provided MAC:</strong></p>
            <div class="hash-output p-2">${response.provided_mac}</div>
            <p class="mt-3 mb-0">
              <small class="text-muted">
                Algorithm: ${response.hash_algorithm} | Type: ${response.mac_type.replace(/_/g, " ").toUpperCase()}
              </small>
            </p>
          </div>
        </div>`;
      const animatedHtml = `<div class="animate__animated animate__fadeInUp">${resultsHtml}</div>`;
    $("#verifyResults").html(animatedHtml);
}


    function displayFileResults(response) {
   const animatedHtml = `<div class="animate__animated animate__fadeInUp">${fullCarouselHtml}</div>`;
    $("#fileResults").html(animatedHtml);
    resultsContainer.empty();

    const algorithms = Object.entries(response.results);

    if (algorithms.length === 0) {
        resultsContainer.html(`<div class="card result-card shadow-sm"><div class="card-body text-center text-muted p-4">No MACs generated for the file.</div></div>`);
        return;
    }

    const carouselId = "fileMacCarousel_" + new Date().getTime();
    let carouselIndicatorsHtml = '';
    let carouselInnerHtml = '';

    algorithms.forEach(([algorithm, methods], index) => {
        carouselIndicatorsHtml += `
          <button type="button" data-bs-target="#${carouselId}" data-bs-slide-to="${index}" class="${index === 0 ? 'active' : ''}" aria-current="${index === 0 ? 'true' : 'false'}" aria-label="Slide ${index + 1} for ${algorithm}"></button>
        `;

        let methodsHtml = '<div class="methods-list p-3">';
        for (const [method, mac] of Object.entries(methods)) {
          methodsHtml += `
            <div class="method-item mb-3">
              <small class="text-muted method-name d-block mb-1">${method.replace(/_/g, " ").toUpperCase()}</small>
              <div class="hash-output p-2">${mac}</div>
            </div>`;
        }
        methodsHtml += '</div>';

        carouselInnerHtml += `
          <div class="carousel-item ${index === 0 ? 'active' : ''}">
            <div class="algorithm-slide-content">
              <h6 class="algorithm-title text-center my-3">
                <span class="badge bg-dark algorithm-badge px-3 py-2">${algorithm.toUpperCase()}</span>
              </h6>
              ${methodsHtml}
            </div>
          </div>
        `;
    });
    
    // Siapkan info file untuk ditampilkan di header kartu
    let fileSizeKB = (response.file_size / 1024).toFixed(2);
    // Buat subjudul yang lebih kecil untuk info file
    const fileInfoSubtitle = `<span class="ms-2 fw-normal text-muted" style="font-size: 0.8em;">for ${response.filename} (${fileSizeKB} KB)</span>`;

    // Rakit HTML carousel lengkap
    const fullCarouselHtml = `
       <div class="card result-card carousel-file-integrity shadow-sm">
        <div class="card-header bg-light border-bottom d-flex justify-content-between align-items-center">
          <h5 class="mb-0">
            <i class="fas fa-file-shield me-2"></i>File Integrity MACs${fileInfoSubtitle}
          </h5>
          <div class="carousel-indicators-container">
              <div class="carousel-indicators m-0 p-0">
                  ${carouselIndicatorsHtml}
              </div>
          </div>
        </div>
        <div class="card-body p-0">
          <div id="${carouselId}" class="carousel slide" data-bs-ride="carousel" data-bs-interval="false">
            <div class="carousel-inner">
              ${carouselInnerHtml}
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#${carouselId}" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Previous Algorithm</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#${carouselId}" data-bs-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Next Algorithm</span>
            </button>
          </div>
        </div>
      </div>
    `;
    resultsContainer.html(fullCarouselHtml);
}
    function displayComparisonResults(response) {
      let resultsHtml = '<div class="row">'; // Container untuk card per algoritma

      const algorithmInfoEntries = Object.entries(response.algorithm_info);

      if(algorithmInfoEntries.length === 0) {
        resultsHtml = `<div class="alert alert-light text-center">No algorithm comparison data available.</div>`;
      } else {
        for (const [algorithm, info] of algorithmInfoEntries) {
            const results = response.results[algorithm] || {}; // Fallback jika tidak ada hasil MAC
            resultsHtml += `
              <div class="col-lg-6 mb-4">
                <div class="card h-100 shadow-sm">
                  <div class="card-header bg-light">
                    <h6 class="mb-0">${algorithm}</h6>
                  </div>
                  <div class="card-body p-3">
                    <p class="mb-1"><small><strong>Output Size:</strong> ${info.output_size || 'N/A'}</small></p>
                    <p class="mb-1"><small><strong>Security:</strong> ${info.security || 'N/A'}</small></p>
                    <p class="mb-2"><small><strong>Speed:</strong> ${info.speed || 'N/A'}</small></p>
                    <hr class="my-2">
                    <p class="mb-1"><small class="text-muted">Sample MAC (Built-in HMAC):</small></p>`;

            const sampleMac = results['builtin_hmac'] || results[Object.keys(results)[0]] || 'N/A';
            resultsHtml += `
                    <div class="hash-output p-2" style="font-size: 0.8em;">${sampleMac}</div>
                  </div>
                </div>
              </div>`;
        }
        resultsHtml += `</div>`; // Akhir dari .row
      }


      resultsHtml += `
        <div class="alert alert-secondary mt-3">
          <h6 class="alert-heading mb-2"><i class="fas fa-info-circle me-1"></i>Comparison Test Data</h6>
          <p class="mb-1 small">The sample MACs above were generated using:</p>
          <small><strong>Test Message:</strong> "${response.test_message}"</small><br>
          <small><strong>Test Key:</strong> "${response.test_key}"</small>
        </div>`;
      const animatedHtml = `<div class="animate__animated animate__fadeInUp">${resultsHtml}</div>`;
    $("#comparisonResults").html(animatedHtml);
    }

    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]:not([data-bs-toggle="tab"])'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

}); // Akhir dari $(document).ready()
