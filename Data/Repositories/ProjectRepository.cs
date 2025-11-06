using dblab1.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace dblab1.Data.Repositories
{
    public class ProjectRepository
    {
        private readonly DbContext _context;

        public ProjectRepository(DbContext context)
        {
            _context = context;
        }

        public void AddProject(Project project)
        {
            using (var cmd = _context.CreateCommand("AddProject"))
            {
                cmd.Parameters.AddWithValue("@project_name", project.ProjectName);
                cmd.Parameters.AddWithValue("@client_id", project.ClientId);
                cmd.Parameters.AddWithValue("@manager_id", project.ManagerId);
                cmd.Parameters.AddWithValue("@status_id", project.StatusId);
                cmd.Parameters.AddWithValue("@team_id", project.TeamId ?? (object)DBNull.Value);
                cmd.Parameters.AddWithValue("@updated_by_user_id", project.UpdatedByUserId ?? (object)DBNull.Value);
                cmd.ExecuteNonQuery();
            }
        }

        public List<ProjectDetails> GetProjectsDetailed()
        {
            var list = new List<ProjectDetails>();
            using (var cmd = _context.CreateCommand("GetProjectsDetailed"))
            using (var reader = cmd.ExecuteReader())
            {
                while (reader.Read())
                {
                    list.Add(new ProjectDetails
                    {
                        ID = (int)reader["ID"],
                        ProjectName = reader["project_name"].ToString(),
                        ClientName = reader["client_name"].ToString(),
                        ManagerName = reader["manager_name"].ToString(),
                        StatusName = reader["project_status"].ToString(),
                        TeamName = reader["team_name"]?.ToString()
                    });
                }
            }
            return list;
        }
    }
}
