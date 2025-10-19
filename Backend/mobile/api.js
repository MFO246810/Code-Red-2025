const API_URL = "http://192.168.1.50:5000"; // replace with your machine's LAN IP later

export async function fetchUsers() {
  const res = await fetch(`${API_URL}/users`);
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}

export async function uploadPhoto(formData) {
  const res = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

