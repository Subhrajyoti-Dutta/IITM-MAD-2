new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        averageRating: 0,
        totalEarnings: 0,
        loading: true,
        searchQuery: "",
        selectedSponsor: "",
        selectedStatus: "All",
        startDate: "",
        endDate: "",
        campaigns: [],
        filteredCampaigns: [],
        sponsors: [],
        modalCampaign: {},
        adPerformance: {},
        isEditing: false,
    },
    methods: {
        fetchData() {
            axios
                .get(`/api/influencer_api/influencer/${this.id}`)
                .then((response) => {
                    this.username = response.data["Username"];
                    this.averageRating = response.data["Rating"];
                    this.totalEarnings = response.data["Earnings"];
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.loading = false;
                });
        },
        fetchSponsors() {
            axios
                .get("/api/sponsor_api/sponsors")
                .then((response) => {
                    this.sponsors = response.data;
                })
                .catch((error) => {
                    console.error("Error fetching sponsors:", error);
                });
        },
        fetchCampaigns() {
            axios
                .get(`/api/influencer_api/influencer/${this.id}/campaigns`)
                .then((response) => {
                    response.data.map((campaign) => {});
                    this.campaigns = response.data;
                    this.filteredCampaigns = response.data;
                    console.log(this.filteredCampaigns);
                })
                .catch((error) => {
                    console.error("Error fetching campaigns:", error);
                });
        },
        filterCampaigns() {
            this.filteredCampaigns = this.campaigns.filter((campaign) => {
                const matchesName = campaign.Name.toLowerCase().includes(
                    this.searchQuery.toLowerCase()
                );
                const matchesSponsor = this.selectedSponsor
                    ? campaign.Sponsor_ID == this.selectedSponsor
                    : true;
                const matchesStatus =
                    this.selectedStatus === "All" ||
                    campaign.Status === this.selectedStatus;
                const matchesStartDate = this.startDate
                    ? new Date(campaign.Start_Date) >= new Date(this.startDate)
                    : true;
                const matchesEndDate = this.endDate
                    ? new Date(campaign.End_Date) <= new Date(this.endDate)
                    : true;

                return (
                    matchesName &&
                    matchesSponsor &&
                    matchesStatus &&
                    matchesStartDate &&
                    matchesEndDate
                );
            });
        },
        viewCampaign(campaign) {
            this.modalCampaign = campaign;
            if (campaign.Status === "Active") {
                this.fetchAdPerformance(campaign.Campaign_ID, campaign.Ad_ID);
            }
            $("#campaignModal").modal("show");
        },
        fetchAdPerformance(campaignId, adId) {
            axios
                .get(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adId}/performance`
                )
                .then((response) => {
                    this.adPerformance = response.data;
                })
                .catch((error) => {
                    console.error("Error fetching ad performance:", error);
                });
        },
        editAdPerformance() {
            this.isEditing = true;
        },
        saveAdPerformance() {
            axios
                .put(
                    `/api/campaign_api/campaign/${this.modalCampaign.Campaign_ID}/adrequest/${this.modalCampaign.Ad_ID}/performance`,
                    this.adPerformance
                )
                .then((response) => {
                    this.adPerformance = response.data;
                    this.isEditing = false;
                })
                .catch((error) => {
                    console.error("Error saving ad performance:", error);
                });
        },
        acceptCampaign(campaignId, adID) {
            axios
                .put(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adID}`,
                    {
                        Status: "Active",
                    }
                )
                .then((response) => {
                    console.log("Campaign accepted:", response);
                    this.fetchCampaigns();
                    $("#campaignModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error accepting campaign:", error);
                });
        },
        rejectCampaign(campaignId, adID) {
            axios

                .put(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adID}`,
                    {
                        Status: "Reject",
                    }
                )
                .then((response) => {
                    console.log("Campaign rejected:", response);
                    this.fetchCampaigns();
                    $("#campaignModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error rejecting campaign:", error);
                });
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.fetchData();
        this.fetchSponsors();
        this.fetchCampaigns();
    },
});
