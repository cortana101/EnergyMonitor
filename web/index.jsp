<%--
  Created by IntelliJ IDEA.
  User: cortana101
  Date: 10/5/15
  Time: 9:02 PM
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
  <head>
    <title></title>
  </head>
  <body>
    Hi this is the test energy monitor program
  <%
    for (int i = 0; i < 10; i++) {
      %> <h2>title <%=Integer.toString(i) %></h2><%
    }
  %>
  </body>
</html>
