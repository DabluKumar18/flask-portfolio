fetch('/api/messages')
  .then(res => res.json())
  .then(data => {
    let rows = '';
    data.forEach(msg => {
      rows += `
        <tr>
          <td>${msg.id}</td>
          <td>${msg.name}</td>
          <td>${msg.email}</td>
          <td>${msg.phone}</td>     <!-- ✅ ADD -->
          <td>${msg.message}</td>
          <td>
            <a href="/delete/${msg.id}"
               onclick="return confirm('Delete this message?')"
               style="color:red;font-weight:bold">
               Delete
            </a>
          </td>
        </tr>`;
    });
    document.getElementById('data').innerHTML = rows;
  });
