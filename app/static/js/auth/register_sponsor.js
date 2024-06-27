new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        username: "",
        password: "",
        full_name: "",
        country_code: "",
        phone: "",
        company: "",
        industry: "",
    },
    methods: {
        register() {
            const data = {
                Username: this.username,
                Password: this.password,
                Full_Name: this.full_name,
                Country_Code: this.country_code,
                Phone: this.phone,
                Company: this.company,
                Industry: this.industry,
            };
            axios
                .post("/api/sponsor_api/sponsor", data)
                .then((response) => {
                    window.location.href = "/auth/login";
                })
                .catch((error) => {
                    console.error(
                        "There was an error registering the sponsor!",
                        error
                    );
                    alert("There was an error registering the sponsor!");
                });
        },
    },
});
