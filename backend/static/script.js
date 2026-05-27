// ===============================
// SWITCH FORMS
// ===============================
function showSignup() {
  document.getElementById("loginForm").classList.add("hidden");
  document.getElementById("signupForm").classList.remove("hidden");
}

function showLogin() {
  document.getElementById("signupForm").classList.add("hidden");
  document.getElementById("loginForm").classList.remove("hidden");
}

// ===============================
// SIGNUP
// ===============================
async function signup() {
  try {
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    const res = await fetch("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    document.getElementById("signupMsg").innerText = data.message;

  } catch (error) {
    console.error("Signup error:", error);
    alert("Signup failed");
  }
}

// ===============================
// LOGIN
// ===============================
async function login() {
  try {
    console.log("Login clicked");

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const res = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    console.log("Login response:", data);

    if (res.ok) {
      window.location.href = "/dashboard";   // ✅ correct
    } else {
      document.getElementById("loginMsg").innerText = data.message;
    }

  } catch (error) {
    console.error("Login error:", error);
    alert("Login failed");
  }
}

// ===============================
// LOGOUT
// ===============================
function logout() {
  window.location.href = "/";   // ✅ FIXED (not index.html)
}

// ===============================
// PREDICT
// ===============================
async function predict() {
  try {
    console.log("Predict clicked");

    const age = document.getElementById("age").value;
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    const ap_hi = document.getElementById("ap_hi").value;
    const ap_lo = document.getElementById("ap_lo").value;

    if (!age || !height || !weight || !ap_hi || !ap_lo) {
      alert("Please fill all fields");
      return;
    }

    const res = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        age: Number(age),
        height: Number(height),
        weight: Number(weight),
        ap_hi: Number(ap_hi),
        ap_lo: Number(ap_lo)
      })
    });

    const data = await res.json();
    console.log("Prediction response:", data);

    alert("Prediction: " + data.prediction);

    // Show result on page
    if (document.getElementById("result")) {
      document.getElementById("result").innerText =
        "Prediction: " + data.prediction;
    }

    // Refresh table + chart
    loadPatients();
    loadChart();

  } catch (error) {
    console.error("Predict error:", error);
    alert("Something went wrong");
  }
}

// ===============================
// LOAD TABLE
// ===============================
async function loadPatients() {
  try {
    const res = await fetch("/patients");
    const data = await res.json();

    let rows = "";

    data.forEach(p => {
      rows += `
        <tr class="border">
          <td class="p-2">${p.age}</td>
          <td class="p-2">${p.height}</td>
          <td class="p-2">${p.weight}</td>
          <td class="p-2">${p.ap_hi}</td>
          <td class="p-2">${p.ap_lo}</td>
          <td class="p-2 font-bold text-blue-600">${p.prediction}</td>
        </tr>
      `;
    });

    if (document.getElementById("tableData")) {
      document.getElementById("tableData").innerHTML = rows;
    }

  } catch (error) {
    console.error("Table error:", error);
  }
}

// ===============================
// LOAD CHART
// ===============================
async function loadChart() {
  try {
    const res = await fetch("/patients");
    const data = await res.json();

    let counts = { Normal: 0, Elevated: 0, Hypertension: 0 };

    data.forEach(p => {
      if (counts[p.prediction] !== undefined) {
        counts[p.prediction]++;
      }
    });

    if (document.getElementById("myChart")) {
      new Chart(document.getElementById("myChart"), {
        type: "bar",
        data: {
          labels: ["Normal", "Elevated", "Hypertension"],
          datasets: [{
            label: "BP Levels",
            data: [counts.Normal, counts.Elevated, counts.Hypertension]
          }]
        }
      });
    }

  } catch (error) {
    console.error("Chart error:", error);
  }
}

// ===============================
// CHATBOT
// ===============================
async function sendMessage() {
  const input = document.getElementById("chatInput");
  const message = input.value.trim();

  if (!message) return;

  const chatBox = document.getElementById("chatBox");

  // USER MESSAGE
  chatBox.innerHTML += `
    <div class="flex justify-end mb-2">
      <div class="bg-blue-600 text-white px-4 py-2 rounded-lg max-w-xs">
        ${message}
      </div>
    </div>
  `;

  input.value = "";

  // BOT LOADING
  chatBox.innerHTML += `
    <div id="typing" class="flex justify-start mb-2">
      <div class="bg-gray-300 px-4 py-2 rounded-lg max-w-xs">
        Typing...
      </div>
    </div>
  `;

  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await res.json();

    // REMOVE TYPING
    document.getElementById("typing").remove();

    // BOT RESPONSE
    chatBox.innerHTML += `
      <div class="flex justify-start mb-2">
        <div class="bg-gray-200 px-4 py-2 rounded-lg max-w-xs">
          ${data.reply}
        </div>
      </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (error) {
    console.error(error);

    document.getElementById("typing").remove();

    chatBox.innerHTML += `
      <div class="text-red-500">Error connecting to chatbot</div>
    `;
  }
}

// ===============================
// AUTO LOAD
// ===============================
window.onload = function () {
  if (document.getElementById("tableData")) {
    loadPatients();
    loadChart();
  }
};
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("chatInput");

  if (input) {
    input.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        sendMessage();
      }
    });
  }
});