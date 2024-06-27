new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        username: "",
        password: "",
        remember: false,
        error: "",
    },
    methods: {
        login() {
            axios
                .post("/auth/login", {
                    username: this.username,
                    password: this.password,
                    remember: this.remember,
                })
                .then((response) => {
                    console.log(response.data);
                    if (response.data.success) {
                        localStorage.setItem("id", response.data.id);
                        window.location.href = response.data.next || "/";
                    } else {
                        console.log(response.data);
                        this.error = response.data.message;
                    }
                })
                .catch((error) => {
                    this.error = "An error occurred. Please try again.";
                });
        },
    },
});
