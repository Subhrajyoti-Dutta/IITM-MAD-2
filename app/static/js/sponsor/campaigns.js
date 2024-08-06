new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        company: "",
        budget: 0,
        loading: true,
        searchQuery: "",
        selectedInfluencer: "",
        selectedStatus: "All",
        startDate: "",
        endDate: "",
        campaigns: [],
        filteredCampaigns: [],
        influencers: [],
        modalCampaign: {},
        modalAd: {},
        newCampaign: {
            Name: "",
            Description: "",
            Budget: 0,
            Start_Date: "",
            End_Date: "",
        },
        newAd: {
            Influencer_ID: 0,
            Topic: "",
            Messages: "",
            Requirements: "",
            Payment_Amount: 0,
            Campaign_ID: 0,
        },
        isEditingCampaign: false,
        isEditingAd: false,
    },
    methods: {
        fetchData() {
            axios
                .get(`/api/sponsor_api/sponsor/${this.id}`)
                .then((response) => {
                    this.username = response.data["Username"];
                    this.company = response.data["Company"];
                    this.budget = response.data["Budget"];
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.loading = false;
                });
        },
        fetchInfluencers() {
            axios
                .get("/api/influencer_api/influencers")
                .then((response) => {
                    this.influencers = response.data;
                })
                .catch((error) => {
                    console.error("Error fetching influencers:", error);
                });
        },
        fetchCampaigns() {
            axios
                .get(`/api/sponsor_api/sponsor/${this.id}/campaigns`)
                .then((response) => {
                    this.campaigns = response.data;
                    this.filteredCampaigns = this.campaigns;
                })
                .catch((error) => {
                    console.error("Error fetching campaigns:", error);
                });
        },
        filterCampaigns() {
            this.filteredCampaigns = this.campaigns
                .map((campaign) => {
                    const matchesName = campaign.Name.toLowerCase().includes(
                        this.searchQuery.toLowerCase()
                    );
                    console.log(matchesName);
                    console.log(campaign.Name.toLowerCase());
                    console.log(this.searchQuery.toLowerCase());
                    const matchesStartDate = this.startDate
                        ? new Date(campaign.Start_Date) >=
                          new Date(this.startDate)
                        : true;
                    const matchesEndDate = this.endDate
                        ? new Date(campaign.End_Date) <= new Date(this.endDate)
                        : true;

                    if (matchesName && matchesStartDate && matchesEndDate) {
                        const filteredAds = campaign.Ads.filter((ad) => {
                            const matchesInfluencer = this.selectedInfluencer
                                ? ad.Influencer_ID == this.selectedInfluencer
                                : true;
                            const matchesStatus =
                                this.selectedStatus === "All" ||
                                ad.Status === this.selectedStatus;
                            return matchesInfluencer && matchesStatus;
                        });
                        return { ...campaign, Ads: filteredAds };
                    }
                    return null;
                })
                .filter((c) => c !== null);
            console.log(this.filteredCampaigns);
        },
        viewCampaign(campaign) {
            this.modalCampaign = { ...campaign };
            this.isEditingCampaign = false;
            $("#campaignModal").modal("show");
        },
        viewAd(campaign, ad) {
            this.modalAd = { ...ad };
            this.modalAd.Flag = this.modalAd.Flag || campaign.Flag;
            this.isEditingAd = false;
            $("#adModal").modal("show");
        },
        openAddCampaignModal() {
            this.newCampaign = {
                Sponsor_ID: this.id,
                Name: "",
                Description: "",
                Budget: 0,
                Start_Date: "",
                End_Date: "",
            };
            $("#addCampaignModal").modal("show");
        },
        addCampaign() {
            this.newCampaign.Budget = +this.newCampaign.Budget;
            axios
                .post("/api/campaign_api/campaign", this.newCampaign)
                .then((response) => {
                    this.fetchCampaigns();
                    $("#addCampaignModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error adding campaign:", error);
                });
        },
        openAddAdModal(campaign) {
            this.newAd = {
                Topic: "",
                Messages: "",
                Requirements: "",
                Payment_Amount: 0,
                Campaign_ID: campaign.Campaign_ID,
                Influencer_ID: 0,
            };
            $("#addAdModal").modal("show");
        },
        addAd() {
            this.newAd.Payment_Amount = +this.newAd.Payment_Amount;
            axios
                .post(
                    `/api/campaign_api/campaign/${this.newAd.Campaign_ID}/adrequest`,
                    this.newAd
                )
                .then((response) => {
                    this.fetchCampaigns();
                    $("#addAdModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error adding ad:", error);
                });
        },
        saveCampaignChanges() {
            axios
                .put(
                    `/api/campaign_api/campaign/${this.modalCampaign.Campaign_ID}`,
                    this.modalCampaign
                )
                .then((response) => {
                    this.fetchCampaigns();
                    this.isEditingCampaign = false;
                    $("#campaignModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error saving campaign changes:", error);
                });
        },
        cancelEditCampaign() {
            this.isEditingCampaign = false;
            $("#campaignModal").modal("hide");
        },
        saveAdChanges() {
            axios
                .put(
                    `/api/campaign_api/campaign/${this.modalAd.Campaign_ID}/adrequest/${this.modalAd.Ad_ID}`,
                    this.modalAd
                )
                .then((response) => {
                    this.fetchCampaigns();
                    this.isEditingAd = false;
                    $("#adModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error saving ad changes:", error);
                });
        },
        cancelEditAd() {
            this.isEditingAd = false;
            $("#adModal").modal("hide");
        },
        deleteCampaign(campaignId) {
            axios
                .delete(`/api/campaign_api/campaign/${campaignId}`)
                .then((response) => {
                    this.fetchCampaigns();
                    $("#campaignModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error deleting campaign:", error);
                });
        },
        deleteAd(campaignId, adId) {
            axios
                .delete(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adId}`
                )
                .then((response) => {
                    this.fetchCampaigns();
                    $("#adModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error deleting ad:", error);
                });
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.fetchData();
        this.fetchInfluencers();
        this.fetchCampaigns();
    },
});
