package delivery.demo.repository;

import delivery.demo.model.Cliente;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ClienteRepository extends JpaRepository<Cliente, Long> {

    // READ
    List<Cliente> findAll();

    Optional<Cliente> findById(Long id);

    // CREATE / UPDATE
    Cliente save(Cliente cliente);

    // DELETE
    void deleteById(Long id);

    // Custom (exemplo)
    List<Cliente> findByNomeContainingIgnoreCase(String nome);

    List<Cliente> findByTelefoneContainingIgnoreCase(String telefone);
}

