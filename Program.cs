using System;
using dblab1.Data;
using dblab1.Models;
using dblab1.Data;
using dblab1.Models;

class Program
{
    static void Main()
    {
        string connStr = "Server=localhost\\SQLEXPRESS;Database=management_system_db;Trusted_Connection=True;TrustServerCertificate=True;";

        using (var uow = new UnitOfWork(connStr))
        {
            var project = new Project
            {
                ProjectName = "CRM Integration",
                ClientId = 3,
                ManagerId = 3,
                StatusId = 1,
                TeamId = null,
                UpdatedByUserId = 4
            };
            uow.Projects.AddProject(project);
            Console.WriteLine("Project added successfully.");

            uow.Tasks.UpdateTaskStatus(1, 2, 2);
            Console.WriteLine("Task status updated.");

            var projects = uow.Projects.GetProjectsDetailed();
            Console.WriteLine("\nProjects List:");
            foreach (var p in projects)
                Console.WriteLine($"{p.ProjectName} — {p.ClientName} — {p.ManagerName} — {p.StatusName}");
        }
    }
}
