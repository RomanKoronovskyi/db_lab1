using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace dblab1.Data.Repositories
{
    public class TaskRepository
    {
        private readonly DbContext _context;

        public TaskRepository(DbContext context)
        {
            _context = context;
        }

        public void UpdateTaskStatus(int taskId, int statusId, int updatedBy)
        {
            using (var cmd = _context.CreateCommand("UpdateTaskStatus"))
            {
                cmd.Parameters.AddWithValue("@task_id", taskId);
                cmd.Parameters.AddWithValue("@status_id", statusId);
                cmd.Parameters.AddWithValue("@updated_by_user_id", updatedBy);
                cmd.ExecuteNonQuery();
            }
        }
    }
}
