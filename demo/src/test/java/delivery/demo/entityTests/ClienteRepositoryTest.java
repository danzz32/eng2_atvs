package delivery.demo.entityTests;

import delivery.demo.model.Cliente;
import delivery.demo.repository.ClienteRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;


import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@ActiveProfiles("test")
@DataJpaTest
public class ClienteRepositoryTest {

    @Autowired
    private ClienteRepository clienteRepository;

    @Test
    @DisplayName("Deve salvar um cliente no db e buscar com êxito")
    void deveSalvarEBuscarCliente() {
        Cliente cliente = new Cliente("Maria", "99999999", "Rua ABC 123");

        Cliente salvo = clienteRepository.save(cliente);
        assertThat(salvo.getId()).isNotNull();
        assertThat(clienteRepository.findById(salvo.getId())).isPresent();
    }

    @Test
    @DisplayName("Deve buscar por nome")
    void deveBuscarPorNome() {
        clienteRepository.save(new Cliente("Marcos", "888888888", "Rua DEF 456"));
        clienteRepository.save(new Cliente("Mariana", "77777777", "Rua GHI 789"));

        List<Cliente> resultado = clienteRepository.findByNomeContainingIgnoreCase("ma");

        assertThat(resultado).hasSize(2);
    }

}
