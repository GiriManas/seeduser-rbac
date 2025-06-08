const handleDownload = async () => {
  if (!results) return;

  try {
    const sessionId = activeSessionId;

    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_API_URL}/topiclensx/download-results`,
      {
        headers: {
          accept: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          "x-access-token": session?.accessToken,
        },
        params: {
          sessionId: sessionId,
        },
        responseType: "blob", // 🔑 This ensures file content is treated as binary
      }
    );

    const blob = new Blob([response.data], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });

    // 🔍 Extract filename from headers
    let filename = "results.xlsx";
    const disposition = response.headers["content-disposition"];
    if (disposition) {
      const match = disposition.match(/filename="?([^"]+)"?/);
      if (match?.[1]) {
        filename = match[1];
      }
    }

    // 📥 Trigger browser download
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Excel download failed:", error);
    alert("Download failed. Check console for details.");
  }
};