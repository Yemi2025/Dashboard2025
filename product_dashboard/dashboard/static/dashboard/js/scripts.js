$(document).ready(function () {
    // Show placeholder on page load
    $("#graph-placeholder").show();
    $("#graph").hide();

    // Autocomplete logic
    $("#company-search").on("input", function () {
        const input = $(this).val().toLowerCase().trim();
        $("#autocomplete-list").empty().hide();
        if (input.length >= 3) {
            const filtered = companies.filter(company => company.toLowerCase().includes(input));
            if (filtered.length > 0) {
                filtered.slice(0, 5).forEach(company => {
                    $("#autocomplete-list").append(
                        `<li class="list-group-item autocomplete-item">${company}</li>`
                    );
                });
                $("#autocomplete-list").show();
            }
        }
    });

    // Handle autocomplete selection
    $("#autocomplete-list").on("click", ".autocomplete-item", function () {
        $("#company-search").val($(this).text().trim());
        $("#autocomplete-list").hide();
    });

    // Handle search button
    $("#search-btn").on("click", function (e) {
        e.preventDefault();
        const companyName = $("#company-search").val().trim();
        const category = $("#category-filter").val();

        if (!companyName) {
            alert("Please select a company first.");
            return;
        }

        // Determine which tab is active
        const activeTab = $(".nav-link.active").attr("href");

        if (activeTab === "#overview") {
            updateGraph(companyName, category);
            $("#graph-container").show(); // Show the graph in Overview
        } else if (activeTab === "#reports") {
            loadReports();
            $("#graph-container").hide(); // Hide the graph in Reports
        } else if (activeTab === "#analytics") {
            loadAnalytics();
            $("#graph-container").hide(); // Hide the graph in Analytics
        }
    });

    // Handle filters
    $("#category-filter").on("change", function () {
        const companyName = $("#company-search").val().trim();
        const category = $(this).val();
        if (!companyName) {
            alert("Please select a company first.");
            return;
        }

        updateGraph(companyName, category);
    });

    // Clear button functionality
    $("#clear-search").on("click", function (e) {
        e.preventDefault();

        // Clear the search bar
        $("#company-search").val("");

        // Clear the autocomplete list
        $("#autocomplete-list").empty().hide();

        // Hide the graph and show the placeholder
        $("#graph").hide();
        $("#graph-placeholder").fadeIn(300);

        // Reset statistics
        $("#total-companies").text("N/A");
        $("#categories").text("N/A");
        $("#hierarchy-depth").text("N/A");

        // Reset company description
        $("#company-description").text("Select a company to view details.");

        // Reset headings
        $("#selected-company-name").text("");
        $("#reports-company-name").text("");
        $("#analytics-company-name").text("");

        // Clear reports & analytics content
        $("#reports-content").html("<p>Please select a company to view reports.</p>");
        $("#analytics-content").html("<p>Please select a company to view analytics data.</p>");
    });

    function updateGraph(company, category = "all") {
        $("#graph-placeholder").fadeIn(300);
        $("#graph").hide();

        $.ajax({
            url: graphDataUrl,
            data: { company_name: company, category: category },
            success: function (response) {
                if (response.plot) {
                    $("#graph").html(response.plot);
                    $("#graph-placeholder").fadeOut(300);
                    $("#graph").css("display", "block").fadeIn(300);

                    if (response.statistics) {
                        $("#total-companies").text(response.statistics.total_companies || "N/A");
                        $("#categories").text(response.statistics.categories || "N/A");
                        $("#hierarchy-depth").text(response.statistics.hierarchy_depth || "N/A");
                    }

                    $("#company-description").text(response.info?.description || "No description available.");
                    $("#selected-company-name").text(company ? `for ${company}` : "");
                    $("#reports-company-name").text(company ? `for ${company}` : "");
                    $("#analytics-company-name").text(company ? `for ${company}` : "");
                } else {
                    alert("Graph data is missing.");
                    $("#graph-placeholder").fadeIn(300);
                    $("#graph").hide();
                }
            },
            error: function (xhr, status, error) {
                console.error("Error fetching graph data:", xhr.responseText);
                alert(`Error fetching graph data: ${error}`);
                $("#graph-placeholder").fadeIn(300);
                $("#graph").hide();
            }
        });
    }

    $(".nav-link").on("click", function (e) {
        e.preventDefault();

        const targetTab = $(this).attr("href");
        $(".tab-pane").removeClass("show active");
        $(targetTab).addClass("show active");

        if (targetTab === "#reports") {
            loadReports();
            $("#graph-container").hide();
            $("#graph").hide();
            $("#graph-placeholder").hide();
        } else if (targetTab === "#overview") {
            $("#graph-container").show();
            const companyName = $("#company-search").val().trim();
            if (companyName) {
                $("#graph").fadeIn(300);
                $("#graph-placeholder").fadeOut(300);
            } else {
                $("#graph-placeholder").show();
            }
        } else if (targetTab === "#analytics") {
            loadAnalytics();
            $("#graph-container").hide();
            $("#graph").hide();
            $("#graph-placeholder").hide();
        }
    });

    function loadReports() {
        const companyName = $("#company-search").val().trim();
        if (!companyName) {
            $("#reports-content").html("<p>Please select a company to view reports.</p>");
            return;
        }

        $.ajax({
            url: "/reports/",
            data: { company_name: companyName },
            success: function (response) {
                $("#reports-content").html(response);
                $("#reports-company-name").text(companyName ? `for ${companyName}` : "");
            },
            error: function () {
                $("#reports-content").html("<p>Error loading reports. Please try again.</p>");
            }
        });
    }

    function loadAnalytics() {
        const companyName = $("#company-search").val().trim();
        if (!companyName) {
            $("#analytics-content").html("<p>Please select a company to view analytics data.</p>");
            return;
        }

        $.ajax({
            url: "/analytics/",
            data: { company_name: companyName },
            success: function (response) {
                if (response.plot) {
                    $("#analytics-content").html(response.plot);
                    $("#analytics-company-name").text(`for ${companyName}`);
                } else {
                    $("#analytics-content").html("<p>No analytics data available.</p>");
                }
            },
            error: function () {
                $("#analytics-content").html("<p>Error loading analytics data. Please try again.</p>");
            }
        });
    }
});
