document.addEventListener("DOMContentLoaded", function () {

    console.log("add_record.js loaded");

    const scenarioMap = {
        "A2": 40,
        "B1": 100,
        "C1": 200,
        "D1": 400,
        "E1": 1000
    };

    const scenario = document.querySelector("[name='scenario']");
    const msgLine = document.querySelector("[name='msg_line']");

    console.log("Scenario =", scenario);
    console.log("Msg Line =", msgLine);

    if (!scenario || !msgLine) {
        console.error("Scenario or Msg Line field not found.");
        return;
    }

    function updateMsgLine() {
        msgLine.value = scenarioMap[scenario.value] || "";
        console.log("Updated Msg Line =", msgLine.value);
    }

    scenario.addEventListener("change", updateMsgLine);

    updateMsgLine();

});