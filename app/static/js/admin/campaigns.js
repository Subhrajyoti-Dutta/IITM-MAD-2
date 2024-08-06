new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        position: "",
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
        currentCampaign: {},
    },
    methods: {
        getData() {
            axios
                .get(`/api/admin_api/admin/${this.id}`)
                .then((response) => {
                    this.username = response.data.Username;
                    this.position = response.data.Position;
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching admin data:", error);
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
                .get(`/api/admin_api/campaigns`)
                .then((response) => {
                    this.campaigns = response.data;
                    // this.filterCampaigns();
                    this.filteredCampaigns = response.data;
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
                .filter((campaign) => campaign && campaign.Ads.length > 0);
        },
        viewCampaign(campaign) {
            this.modalCampaign = { ...campaign };
            this.isEditingCampaign = false;
            $("#campaignModal").modal("show");
        },
        viewAd(campaign, ad) {
            this.modalAd = { ...ad };
            this.modalAd.Campaign_ID = campaign.Campaign_ID;
            console.log(this.modalAd);
            this.isEditingAd = false;
            $("#adModal").modal("show");
        },
        closeAd() {
            this.isEditingAd = false;
            $("#adModal").modal("hide");
        },
        flagCampaign(campaignId) {
            axios
                .put(`/api/admin_api/campaign/${campaignId}`, {
                    Flag: true,
                })
                .then((response) => {
                    this.modalCampaign.Flag = true;
                    this.updateCampaignInList(campaignId, true);
                })
                .catch((error) => {
                    console.error("Error flagging campaign:", error);
                });
        },
        deflagCampaign(campaignId) {
            axios
                .put(`/api/admin_api/campaign/${campaignId}`, {
                    Flag: false,
                })
                .then((response) => {
                    this.modalCampaign.Flag = false;
                    this.updateCampaignInList(campaignId, false);
                })
                .catch((error) => {
                    console.error("Error deflagging campaign:", error);
                });
        },
        flagAd(campaignId, adId) {
            axios
                .put(`/api/admin_api/campaign/${campaignId}/ad/${adId}`, {
                    Flag: true,
                })
                .then((response) => {
                    this.modalAd.Flag = true;
                    this.updateAdInList(adId, true);
                })
                .catch((error) => {
                    console.error("Error flagging ad:", error);
                });
        },
        deflagAd(campaignId, adId) {
            axios
                .put(`/api/admin_api/campaign/${campaignId}/ad/${adId}`, {
                    Flag: false,
                })
                .then((response) => {
                    this.modalAd.Flag = false;
                    this.updateAdInList(adId, false);
                })
                .catch((error) => {
                    console.error("Error deflagging ad:", error);
                });
        },
        updateCampaignInList(campaignId, flag) {
            const campaign = this.campaigns.find(
                (c) => c.Campaign_ID === campaignId
            );
            if (campaign) {
                campaign.Flag = flag;
            }
            this.filterCampaigns();
        },
        updateAdInList(adId, flag) {
            const campaign = this.campaigns.find((c) =>
                c.Ads.find((ad) => ad.Ad_ID === adId)
            );
            if (campaign) {
                const ad = campaign.Ads.find((ad) => ad.Ad_ID === adId);
                if (ad) {
                    ad.Flag = flag;
                }
            }
        },
        collapseCampaign(campaign) {
            campaign.Expand = false;
            this.currentCampaign.Expand = false;
            this.id = this.id + 1;
            this.id = this.id - 1;
        },
        expandCampaign(campaign) {
            this.currentCampaign.Expand = false;
            this.currentCampaign = campaign;
            this.currentCampaign.Expand = true;
            this.id = this.id + 1;
            this.id = this.id - 1;
        },
    },
    created() {
        this.id = +localStorage.getItem("id");
        this.getData();
        this.fetchInfluencers();
        this.fetchCampaigns();
    },
    mounted() {
        this.filteredCampaigns = this.campaigns;
    },
});
